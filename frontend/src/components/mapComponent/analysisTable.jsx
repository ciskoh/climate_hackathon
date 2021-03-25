import React from 'react';

import { Box, DataTable, Meter, Text } from 'grommet';
import geojsonFile from '../../assets/test_aoi_valencia_subpolygon_but_json.json';


let columns = [
  {
    property: 'id',
    header: <Text>ID</Text>,
    sortable: true,
    size: 'xxsmall',

  },
  {
    property: 'land_cover',
    header: <Text>Land cover</Text>,
    sortable: true,
    size: 'xsmall',
  },
  {
    property: 'land_management',
    header: <Text>Management tyoe</Text>,
    sortable: true,
    size: 'small',
  },
  {
    property: 'co2_metric_1',
    header: 'co2_metric_1',
    sortable: true,
    size: '',
    render: datum => (
      <Box pad={{ vertical: 'xsmall' }}>
        <Meter
          values={[{ value: datum.co2_metric_1 }]}
          thickness="small"
          size="small"
        />
      </Box>
    ),
  },
]

// console.log(geojsonFile);
const tempData = geojsonFile;
const tempFeatures = geojsonFile.features
const tableName = tempData.name
export let tempCoordinates = [];

let polyColor = landCover => {
  // console.log('from lopycolor function',feature.landCover);
  if (landCover === 'Built-up') return "gray"; 
  if (landCover === 'Crop 1') return "yellow";
  if (landCover === 'Crop 2') return "lightblue";
  if (landCover === 'Crop 3') return "lightgreen";
  if (landCover === 'Fallow') return "lightbrown";
  if (landCover === 'Forest') return "darkgreen";
}


tempFeatures.forEach(feature =>{ 
  const tempFeature = {id: feature.properties.id, polygonName: feature.properties.land_cover, landCover: polyColor(feature.properties.land_cover) ,coordinates: feature.geometry.coordinates[0][0]};
  // console.log(tempFeature);
  tempFeature.coordinates.forEach(coordinates => {
    let tempLat = coordinates[0];
    coordinates[0] = coordinates[1];
    coordinates[1] = tempLat

  })
  tempCoordinates.push(tempFeature)  
});

let DATA = [];
tempFeatures.forEach(feature => 
  DATA.push(feature.properties)  
)

// console.log('the temp coord', tempCoordinates);

const AnalysisTable = () => (

      <Box align="center" pad="medium" height='100%'>
        <Text weight='bold'>{tableName}</Text>
        <DataTable 
          sortable 
          columns={columns} 
          data={DATA} 
          size="100%"
        />
      </Box>
);

export default AnalysisTable;