import { useState, useEffect } from "react";
import "./App.css";
import TrafficSign from "./assets/trafficsign.png";

const App = () => {
  // Map every traffic sign prediction class to its corresponding image
  const trafficSignMap = {
    0: TrafficSign,
    1: TrafficSign,
    2: TrafficSign,
    3: TrafficSign,
  };

  // Initialize App State
  const [speedSign, setSpeedSign] = useState(0);
  const [dangerLongSign, setDangerLongSign] = useState(0);
  const [dangerShortSign, setDangerShortSign] = useState(0);
  const [giveWaySign, setGiveWaySign] = useState(0);

  // Define API call to the YOLOv7 backend for real-time rendering
  const fetchData = async () => {
    console.log("UPDATE ", Date.now())
    /*await fetch("http://localhost:8080/getCurrentPredictions/")
      .then((response) => {
        response.json();
      })
      .then((data) => {
        if (!(data.speedSign === speedSign)) {
          setSpeedSign(data.speedSign);
        }
        if (!(data.dangerLongSign === dangerLongSign)) {
          setDangerLongSign(data.dangerLongSign);
        }
        if (!(data.dangerShortSign === dangerShortSign)) {
          setDangerShortSign(data.dangerShortSign);
        }
        if (!(data.giveWaySign === giveWaySign)) {
          setGiveWaySign(data.giveWaySign);
        }
      })
      .catch((err) => {
        console.log(err);
      });*/
  };

  // useEffect hook: update the UI by calling fetchData every 100 milliseconds
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, 300);

    // componentWillUnmount cleanup
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>DriveAssist</h1>

      <div className="grid2x2">
        <div>
          <img className="panel" src={trafficSignMap[speedSign]} alt="Traffic Sign"/>
        </div>
        <div>
          <img className="panel" src={trafficSignMap[dangerLongSign]} alt="Traffic Sign"/>
        </div>
        <div>
          <img className="panel" src={trafficSignMap[dangerShortSign]} alt="Traffic Sign"/>
        </div>
        <div>
          <img className="panel" src={trafficSignMap[giveWaySign]} alt="Traffic Sign"/>
        </div>
      </div>
    </div>
  );
};

export default App;
