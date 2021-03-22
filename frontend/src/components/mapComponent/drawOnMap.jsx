import React, { useRef, useEffect, useState } from "react";
import { Map as MapContainer, TileLayer, FeatureGroup, Marker, Popup } from 'react-leaflet';
import { EditControl } from "react-leaflet-draw";

import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";

import L from "leaflet";


const maptiles = [
  'http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}',
  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
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
    console.log(mapMarkings);
  return (
    <>
        <MapContainer 
            center={position} 
            zoom={zoom} 
            style={{ width: '100%', height: '900px'}}
            ref={mapRef}
        >
          <FeatureGroup>
            <EditControl
              position="topright"
              onCreated={onCreateHandler}
              onEdited={ onEditHandler}
              onDeleted={ onDeleteHandler}
              draw={{
                rectangle: false,
                polyline: false,
                circle: false,
                circlemarker: false,
                marker: false,
              }}
            />
          </FeatureGroup>
        <TileLayer
        attribution='&copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url={maptiles[1]}
        />
        </MapContainer>
           <pre className="text-left">{JSON.stringify(mapMarkings, 0, 2)}</pre>
    </>
  );
};

export default LeafLetMap;