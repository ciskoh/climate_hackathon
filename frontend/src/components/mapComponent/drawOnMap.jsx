import React, { useRef, useState } from "react";
import { Box, Button } from "grommet";

// ====================== leaflet ==========================
import { FeatureGroup, GeoJSON, Layer, LayersControl, Map as MapContainer, Polygon, TileLayer} from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";

import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";

import Control from 'react-leaflet-control';
// ========================================================= 
// ====================== map layers ======================= 
import { mapTiles } from './mapLayers';
// ========================================================= 
// ======================  temp stuff ====================== 
import test_aoi_valencia from '../../assets/test_aoi_valencia.geojson';
import test_aoi_valencia_subpolygon from '../../assets/test_aoi_valencia_subpolygon.geojson';

import test_aoi_valencia_subpolygon_but_json from '../../assets/test_aoi_valencia_subpolygon_but_json.json';

import { temporalPolygon } from './experimetalPolygon';
import AnalysisTable from "./analysisTable";

let valenciaQ = [ -0.490210232840616, 39.652317010415992 ];
// =========================================================



const LeafLetMap = () => {
  const [ position, setPosition] = useState([47.07, 8.325]);
  const [ mapMarkings, setMapMarkings ] = useState([]);
  let zoom = 12;
  const mapRef = useRef()

  const onCreateHandler = (event) => {
    console.log(event);
    const { layerType, layer } = event;
    if (layerType === 'polygon') {
      const { _leaflet_id } = layer;

      setMapMarkings(layers => [ 
        ...layers,
        { id: _leaflet_id, latlngs: layer.getLatLngs()[0] }
      ])
    }
  };
  const onEditHandler = (event) => {
    console.log(event);
    const { layers: { _layers } } = event;
    // eslint-disable-next-line array-callback-return
    Object.values( _layers).map( ({_leaflet_id, editing}) => {
      setMapMarkings( layers => 
        layers.map( layer => 
          layer.id === _leaflet_id ? 
          { ...layer, latlngs: { ...editing.latlngs[0] } } : layer ) )
    } );

  };
  const onDeleteHandler = (event) => {
    console.log(event);
    const { layers: { _layers } } = event;

    // eslint-disable-next-line array-callback-return
    Object.values( _layers).map( ({_leaflet_id }) => {
      setMapMarkings( layers => layers.filter( layer => layer.id !== _leaflet_id));
    });
  };

  // console.log(JSON.stringify(mapMarkings));
  let polygonsMarked = JSON.stringify(mapMarkings, 0, 2)


  // let polyStyles = feature => {
  //     switch (feature.properties.land_cover) {
  //         case 'Built-up': return {color: "gray"};
  //         case 'Crop 1':   return {color: "yellow"};
  //         case 'Crop 2':   return {color: "lightblue"};
  //         case 'Crop 3':   return {color: "lightgreen"};
  //         case 'Fallow':   return {color: "lightbrown"};
  //         case 'Forest':   return {color: "darkgreen"};
  //         default: return {color: "darkgreen"};
  //   }
  // }



  return (
    <Box width="xlarge" height="large" margin='xsmall' alignSelf='center' direction='row' >
      <Box elevation='medium' height='100%' width="75vw" pad='xsmall' border>
        <MapContainer style={ { width: '100%', height: '900px' } }
          center={ position } zoom={ zoom } ref={ mapRef }
        >
          <FeatureGroup>
            <EditControl
              position="topright"
              onCreated={ onCreateHandler }
              onEdited={ onEditHandler }
              onDeleted={ onDeleteHandler }
              draw={{
                rectangle: false,
                polyline: false,
                circle: false,
                circlemarker: false,
                marker: false,
              }}
            />
          </FeatureGroup>          
          <LayersControl position="topleft">
            <LayersControl.BaseLayer checked name={`${mapTiles[0].name}`}>
              <TileLayer attribution={`${mapTiles[0].attribution}`} url={`${mapTiles[0].url}`}/>
            </LayersControl.BaseLayer> 
            <LayersControl.BaseLayer name={`${mapTiles[1].name}`}>
              <TileLayer attribution={`${mapTiles[1].attribution}`} url={`${mapTiles[1].url}`}/>
            </LayersControl.BaseLayer> 
            <LayersControl.BaseLayer name={`${mapTiles[2].name}`}>
              <TileLayer attribution={`${mapTiles[2].attribution}`} url={`${mapTiles[2].url}`}/>
            </LayersControl.BaseLayer> 
            <LayersControl.Overlay name="tempLayer">
          <Polygon positions={ temporalPolygon } color='black'/>
            </LayersControl.Overlay>
          </LayersControl>
          {
            test_aoi_valencia_subpolygon_but_json.features.map(feature => 
              <Polygon key={feature.properties.id} positions={ feature.geometry.coordinates } />
              )
          }
        </MapContainer>
      </Box>

      <Box margin={{left: 'small'}} width='25vw' align='center' >

        <Box elevation='medium' round='medium' margin='small' height='xsmall' width='small'>
          <Button fill label='print' onClick={ () => console.log(polygonsMarked.length === 2 ? 'Please mark on the map' : polygonsMarked) }/>
        </Box>  
        <Box elevation='medium' width='100%'>
          <AnalysisTable />
        </Box>
      </Box>

    </Box>
  );
};

export default LeafLetMap;