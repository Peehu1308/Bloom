import logo from './logo.svg';
import './App.css';
import Box from './components/box_plants';
import './index.css'
import Box_grid from './components/box_grid';
import { Plants_screen } from './components/plants_screen';
import VegetationData from './components/vegetationdata';
import LowVegetationData from './components/low_vegetation';
import CountryTrendChart from './components/country';
import PlantClassifier from './components/plantclassifier';
import Conservation_box from './components/conservation_box';
import { Conservation_screen } from './components/conservation_screen';
import FlowerPredictor from './components/prediction_cnn';
import VegetationGlobe from './components/vegetation_globe';
import VegetationHeatmapGlobe from './components/type_vegetationglobe';
import GlobeWithTexture from './components/globewithtexture';
import TypesvegetationGlobe from './components/globewithtexture';
import TypeVegetationGlobe from './components/globewithtexture';
import CitizenObservationForm from './components/input_form';
import GlobeWithObservations from './components/input_observations';
import ObservationsList from './components/input_observations';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <CountryTrendChart/> */}
        {/* <VegetationData/> */}
        {/* <LowVegetationData/> */}
        {/* <Conservation_screen/> */}
        {/* <FlowerPredictor/> */}
        {/* <VegetationGlobe/> */}
        {/* <VegetationHeatmapGlobe/> */}
        {/* <GlobeWithTexture/> */}
        {/* <TypeVegetationGlobe/> */}
        <h1>BloomWatch Citizen Science</h1>
      <CitizenObservationForm/>
      <ObservationsList/>
        {/* <PlantClassifier/> */}

      </header>
    </div>
  );
}

export default App;
