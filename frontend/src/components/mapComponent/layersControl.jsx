import React from 'react';
import { LayersControl, TileLayer } from 'react-leaflet';



const LayerControlButton = (props) => {
    let maps = props.maps;
    console.log('from layer control props', props);
    console.log('from layer control maps', maps);
    return (
        <>
            <LayersControl position="topleft">
                {
                    maps.map((map, index) => {
                        index === 0 ? 
                        <LayersControl.BaseLayer checked name={ map.name }>
                            <TileLayer
                                attribution={ map.attribution }
                                url={ map.url }
                            />
                         </LayersControl.BaseLayer>
                        :
                        <LayersControl.BaseLayer name={ map.name }>
                            <TileLayer
                                attribution={ map.attribution }
                                url={ map.url }
                            />
                         </LayersControl.BaseLayer>
                    })
                }

            </LayersControl>
        </>
    );
};

export default LayerControlButton;