import React, { useRef, useState } from "react";
import { Map as MapContainer, TileLayer, FeatureGroup, LayersControl } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";

import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import { Box, Button } from "grommet";

import L from 'leaflet';

import Control from 'react-leaflet-control';
import test_aoi_valencia from '../../assets/test_aoi_valencia.geojson';
import test_aoi_valencia_subpolygon from '../../assets/test_aoi_valencia_subpolygon.geojson';
import LayerControlButton from "./layersControl";


const mapTiles = [
  {
    name: 'OpenStreetMap',
    attribution: '&copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  },
  {
    name: 'GoogleMaps - Terrain',
    attribution: '&copy <a href="https://about.google/brand-resource-center/products-and-services/geo-guidelines/#google-earth">GoogleMaps</a> Data 2021',
    url: 'http://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}'
  },
  {
    name: 'GoogleMaps Sattelite',
    attribution: '&copy <a href="https://about.google/brand-resource-center/products-and-services/geo-guidelines/#google-earth">GoogleMaps</a> Data 2021',
    url: 'http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}'
  },
]

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

      Object.values( _layers).map( ({_leaflet_id }) => {
        setMapMarkings( layers => layers.filter( layer => layer.id !== _leaflet_id));
      });
    };
    // console.log(JSON.stringify(mapMarkings));
    let polygonsMarked = JSON.stringify(mapMarkings, 0, 2)

    // L.geoJSON(states, {
    //   style: function(feature) {
    //       switch (feature.properties.party) {
    //           case 'Built-up': return {color: "gray"};
    //           case 'Crop 1':   return {color: "yellow"};
    //           case 'Crop 2':   return {color: "lightblue"};
    //           case 'Crop 3':   return {color: "lightgreen"};
    //           case 'Fallow':   return {color: "lightbrown"};
    //           case 'Forest':   return {color: "darkgreen"};
    //       }
    //   }
  // }).addTo(map);


  return (
    <Box
    width="xlarge" 
    height="medium"
    margin='small'
    alignSelf='center'
    direction='row'
    >
      <Box width="xlarge" height="large" pad='xsmall' border>
        <MapContainer 
            center={ position } 
            zoom={ zoom } 
            style={ { width: '100%', height: '900px' } }
            ref={ mapRef }
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
          </LayersControl>
        </MapContainer>
      </Box>
           <Box margin='small' height='xsmall' width='small'>
            <Button fill label='print' onClick={ () => console.log(polygonsMarked.length === 2 ? 'Please mark on the map' : polygonsMarked) }/>
          </Box>  
    </Box>
  );
};

export default LeafLetMap;