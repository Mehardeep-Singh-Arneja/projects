import "./App.css";

import Telemetry from "./components/Telemetry/Telemetry";
import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Problem from "./components/Problem/Problem";
import Objectives from "./components/Objectives/Objectives";
import Approach from "./components/Approach/Approach";
import Results from "./components/Results/Results";
import Timeline from "./components/Timeline/Timeline";
import Team from "./components/Team/Team";
import Footer from "./components/Footer/Footer";
import ForecastAnimations from "./components/ForecastAnimations/ForecastAnimations";

function App() {
  return (
    <div className="app">

      <Telemetry />

      <Navbar />

      <Hero />

      <Problem />

      <Objectives />

      <Approach />

      <Results />

      <ForecastAnimations />

      <Timeline />

      <Team />

      {/* <Footer /> */}

    </div>
  );
}

export default App;