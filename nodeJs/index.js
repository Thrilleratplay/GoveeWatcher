/*
 * Proof of concept bluetooth broadcast decoder from Govee H5075 Thermometer Hygrometer using bluez
 *
 * Copyright (c) 2019 - Tom Hiller
 */

/* eslint-disable no-console */
const os = require('os');
const fs = require('fs');

const nodeCleanup = require('node-cleanup');
const pty = require('node-pty');
const ransi = require('strip-ansi');

// ***************************************************************

const DEBUG = false;

if (DEBUG) {
  /* eslint-disable-next-line no-unused-vars */
  const logStream = fs.createWriteStream('dataoutput.log', { flags: 'a' });
}

// ***************************************************************

const DEGREE_CHAR = String.fromCharCode(176);

const TAG_REGEX = '([[A-Z]{3,5}])?';
const MAC_REGEX = '([0-9A-F]{1,2}[.:-][0-9A-F]{1,2}[.:-][0-9A-F]{1,2}[.:-][0-9A-F]{1,2}[.:-][0-9A-F]{1,2}[.:-][0-9A-F]{1,2})';
const BROADCAST_REGEX = new RegExp([
  TAG_REGEX,
  '\\s?',
  'Device',
  '\\s?',
  MAC_REGEX,
  '\\s?',
  '(.*)',
].join(''), 'gm');
const HEX_DATA_REGEX = new RegExp('([0-9a-f]{2}\\s?)*', 'gm');

// ***************************************************************

const devices = {};
const deviceRSSI = {};

/**
 * Remove terminal styling, nonprintable control characters and carriage return
 * @param {string} str Drity string
 * @returns {string} Clean string
 */
/* eslint-disable-next-line no-control-regex */
const sanitize = (str) => ransi(str).replace(/\u0001\u0002/g, '').replace(/\r/g, '');

/**
 * create a terminal and start scanning
 */
const term = pty.spawn('bluetoothctl', ['scan', 'on'], {
  name: 'xterm-mono',
  cols: 100,
  rows: 40,
  cwd: process.env.HOME,
  env: process.env,
});

// On data event
term.on('data', (rawData) => {
  const data = sanitize(rawData);

  const broadcastMatch = BROADCAST_REGEX.exec(data);
  const dataMatch = HEX_DATA_REGEX.exec(data);

  let streamUpdate;
  let encodedData;
  let tempInC;
  let tempInF;
  let humidityPercentage;

  let btMAC;
  let broadcastData;
  let tag;

  // Matches the boardcast regex
  if (broadcastMatch) {
    /* eslint-disable prefer-destructuring */
    btMAC = broadcastMatch[2];
    tag = broadcastMatch[1];
    broadcastData = broadcastMatch[3];
    /* eslint-enable prefer-destructuring */

    // Newly discovered devices
    if (tag === '[NEW]') {
      devices[btMAC] = broadcastData;
      console.log(`Found: ${btMAC} (${broadcastData})`);
    // Device signal strength
    } else if (tag === '[CHG]' && broadcastData.startsWith('RSSI')) {
      deviceRSSI[btMAC] = deviceRSSI[btMAC] || [];
      deviceRSSI[btMAC].push(broadcastData.replace('RSSI:', '').trim());
      console.log(`${devices[btMAC]} -  ${broadcastData}`);
    // Has "ManufacturerData Key" for Govee Thermohydrometer
    } else if (data.includes('0xec88')) {
      // Look for two character strings which should be a hex octet
      streamUpdate = data.split(' ').filter((x) => String(x).trim().length === 2);

      if (streamUpdate.length > 4) {
        // The first octet is 00, the next four are encoded with
        // the temperature in C and humidity Percentage.
        // TODO: figure out the battery life percentage
        encodedData = parseInt(streamUpdate.slice(1, 4).join(''), 16);
        tempInC = (encodedData / 10000).toPrecision(3);
        tempInF = ((tempInC * 1.8) + 32).toPrecision(3);
        humidityPercentage = ((encodedData % 1000) / 10).toPrecision(3);

        console.log([
          devices[btMAC] || 'Govee Thermohydrometer',
          ' - ',
          'Temp: ',
          tempInC,
          DEGREE_CHAR,
          'C',
          ' / ',
          tempInF,
          DEGREE_CHAR,
          'F',
          ' - ',
          'Humidity: ',
          humidityPercentage,
          '%',
        ].join(''));
      }
    }
  } else if (dataMatch && DEBUG) {
    console.log(dataMatch);
  }

  if (DEBUG) {
    console.log(data);

    /* eslint-disable-next-line no-undef */
    logStream.write(sanitize(data) + os.EOL);
  }
});

// Turn off the lights when you leave a room
nodeCleanup(() => {
  term.write('bluetoothctl scan off && exit\r');
});
