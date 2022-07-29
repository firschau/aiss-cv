import { useState, useEffect } from "react";
import "./App.css";

import DrivelyLogo from "./assets/drively.png";

import _0 from "./assets/0.png";
import _1 from "./assets/1.png";
import _2 from "./assets/2.png";
import _3 from "./assets/3.png";
import _4 from "./assets/4.png";
import _5 from "./assets/5.png";
import _6 from "./assets/6.png";
import _7 from "./assets/7.png";
import _8 from "./assets/8.png";
import _9 from "./assets/9.png";
import _10 from "./assets/10.png";
import _11 from "./assets/11.png";
import _12 from "./assets/12.png";
import _13 from "./assets/13.png";
import _14 from "./assets/14.png";
import _15 from "./assets/15.png";
import _16 from "./assets/16.png";
import _17 from "./assets/17.png";
import _18 from "./assets/18.png";
import _19 from "./assets/19.png";
import _20 from "./assets/20.png";
import _21 from "./assets/21.png";
import _22 from "./assets/22.png";
import _23 from "./assets/23.png";
import _24 from "./assets/24.png";
import _25 from "./assets/25.png";
import _26 from "./assets/26.png";
import _27 from "./assets/27.png";
import _28 from "./assets/28.png";
import _29 from "./assets/29.png";
import _30 from "./assets/30.png";
import _31 from "./assets/31.png";
import _32 from "./assets/32.png";
import _33 from "./assets/33.png";
import _34 from "./assets/34.png";
import _35 from "./assets/35.png";
import _36 from "./assets/36.png";
import _37 from "./assets/37.png";
import _38 from "./assets/38.png";
import _39 from "./assets/39.png";
import _40 from "./assets/40.png";
import _41 from "./assets/41.png";
import _42 from "./assets/42.png";
import _43 from "./assets/43.jpeg";
import _44 from "./assets/44.jpeg";
import _45 from "./assets/45.jpeg";
import Placeholder from "./assets/placeholder.png";

// Map every traffic sign class to its corresponding image
const trafficSignMap = {
  0: _0,
  1: _1,
  2: _2,
  3: _3,
  4: _4,
  5: _5,
  6: _6,
  7: _7,
  8: _8,
  9: _9,
  10: _10,
  11: _11,
  12: _12,
  13: _13,
  14: _14,
  15: _15,
  16: _16,
  17: _17,
  18: _18,
  19: _19,
  20: _20,
  21: _21,
  22: _22,
  23: _23,
  24: _24,
  25: _25,
  26: _26,
  27: _27,
  28: _28,
  29: _29,
  30: _30,
  31: _31,
  32: _32,
  33: _33,
  34: _34,
  35: _35,
  36: _36,
  37: _37,
  38: _38,
  39: _39,
  40: _40,
  41: _41,
  42: _42,
  43: _43,
  44: _44,
  99: Placeholder,
};

const App = () => {
  // Initialize App State
  const [speedSign, setSpeedSign] = useState(99);
  const [dangerLongSign, setDangerLongSign] = useState(99);
  const [dangerShortSign, setDangerShortSign] = useState(99);
  const [giveWaySign, setGiveWaySign] = useState(99);
  const [person, setPerson] = useState(false);

  // Define API call to the YOLOv7 backend for real-time rendering
  const fetchData = async () => {
    console.log("UPDATE ", Date.now());
    await fetch("https://guarded-meadow-37802.herokuapp.com/http://127.0.0.1:5000/inference")
      .then((response) => {
        response.json();
      })
      .then((data) => {
        if (!(data.slot_1 === speedSign)) {
          setSpeedSign(data.slot_1);
        }
        if (!(data.slot_2 === dangerLongSign)) {
          setDangerLongSign(data.slot_2);
        }
        if (!(data.slot_3 === dangerShortSign)) {
          setDangerShortSign(data.slot_3);
        }
        if (!(data.slot_4 === giveWaySign)) {
          setGiveWaySign(data.slot_4);
        }
        if (!(data.person === person)) {
          setPerson(data.person);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // useEffect hook: update the UI by calling fetchData every 100 milliseconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, 300);

    // componentWillUnmount cleanup
    return () => clearInterval(interval);
  }, []);

  const dynamicBackgroundColor = person ? "red" : "#f7f7f7";

  return (
    <div className="App" style={{ backgroundColor: dynamicBackgroundColor }}>
      <img src={DrivelyLogo} className="app-logo" />

      <div className="sign-container">
        {speedSign ? (
          <img
            className="panel"
            src={trafficSignMap[speedSign]}
            alt="Traffic Sign"
          />
        ) : (
          <img src={Placeholder} className="panel"></img>
        )}

        <div className="vertical-divider" />

        {dangerLongSign ? (
          <img
            className="panel"
            src={trafficSignMap[dangerLongSign]}
            alt="Traffic Sign"
          />
        ) : (
          <img src={Placeholder} className="panel"></img>
        )}

        <div className="vertical-divider" />

        {dangerShortSign ? (
          <img
            className="panel"
            src={trafficSignMap[dangerShortSign]}
            alt="Traffic Sign"
          />
        ) : (
          <img src={Placeholder} className="panel"></img>
        )}

        <div className="vertical-divider" />

        {giveWaySign ? (
          <img
            className="panel"
            src={trafficSignMap[giveWaySign]}
            alt="Traffic Sign"
          />
        ) : (
          <img src={Placeholder} className="panel"></img>
        )}
      </div>

      {person && <h1>ATTENTION</h1>}
    </div>
  );
};

export default App;
