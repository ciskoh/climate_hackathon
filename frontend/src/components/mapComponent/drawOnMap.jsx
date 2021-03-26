import React, { useRef, useState, Fragment } from "react";
import { Box, Button } from "grommet";

// ====================== leaflet ==========================
import { FeatureGroup, LayersControl, Map as MapContainer, Polygon, TileLayer} from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";

import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";

// ========================================================= 
// ====================== map layers ======================= 
import { mapTiles } from './mapLayers';
// ========================================================= 
// ======================  temp stuff ====================== 

import { temporalPolygon } from './experimetalPolygon';
import AnalysisTable from "./analysisTable";

// =========================================================
let polyColor = landCover => {
  if (landCover === 'Built-up') return "gray"; 
  if (landCover === 'Crop 1') return "yellow";
  if (landCover === 'Crop 2') return "lightblue";
  if (landCover === 'Crop 3') return "lightgreen";
  if (landCover === 'Fallow') return "lightbrown";
  if (landCover === 'Forest') return "darkgreen";
}


const LeafLetMap = () => {
  const [ position ] = useState([47.07, 8.325]);
  const [ mapMarkings, setMapMarkings ] = useState([]);
  const [ results, setResults ] = useState({});
  const [ tempCoordinates, setTempCoordinates ] = useState([])
  let zoom = 12;
  const mapRef = useRef()


  const onCreateHandler = (event) => {
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
    const { layers: { _layers } } = event;
    Object.values( _layers).map( ({_leaflet_id, editing}) => {
      setMapMarkings( layers => 
        layers.map( layer => 
          layer.id === _leaflet_id ? 
          { ...layer, latlngs: { ...editing.latlngs[0] } } : layer ) )
    } );

  };
  const onDeleteHandler = (event) => {
    const { layers: { _layers } } = event;
    Object.values( _layers).map( ({_leaflet_id }) => {
      setMapMarkings( layers => layers.filter( layer => layer.id !== _leaflet_id));
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const url = `http://localhost:8000/backend/api/maps/new/`;
    const config = {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ "coordinates": mapMarkings[0] }),
    };

    fetch(url, config)
      .then((response) => response.json())
      .then((data) => {
        setResults(data)
        let inverted = []
        const tempFeatures = data.data.features
        tempFeatures.forEach(feature =>{ 
          const tempFeature = {id: feature.properties.id, polygonName: feature.properties.land_cover, landCover: polyColor(feature.properties.land_cover) ,coordinates: feature.geometry.coordinates[0][0]};
          tempFeature.coordinates.forEach(coordinates => {
            let tempLat = coordinates[0];
            coordinates[0] = coordinates[1];
            coordinates[1] = tempLat
          })
          inverted.push(tempFeature)  
        })
        setTempCoordinates(inverted)
        })
  };






  return (
    <>
      <Box width="95vw" height="large" margin='xsmall' alignSelf='center' direction='coulumn' >
        <Box elevation='medium' height='100%' width="60vw" pad='xsmall' border>
          <MapContainer style={ { width: '100%', height: '100%' } }
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
                {
                  tempCoordinates.map(feature => 
              <LayersControl.Overlay name={`${feature.polygonName}`}>
                    <Polygon key={feature.id} positions={ feature.coordinates } color={ feature.landCover }/>
              </LayersControl.Overlay>
                  )
                }

            </LayersControl>
          </MapContainer>
        </Box>

          <Box elevation='medium' width='40vw' height='100%' border>
            {
              Object.entries(results).length === 0 ? 
              null
              : <AnalysisTable results={results.data}/>
            }
            <Box margin={{left: 'small'}} width='90vw' align='center' >
              <Box elevation='medium' round='medium' margin='small' height='xsmall' width='small'>
                <Button fill label='Submit Polygon' onClick={handleSubmit}/>
              </Box>
            </Box>  
          </Box>

      </Box>
    </>
  );
};

export default LeafLetMap;