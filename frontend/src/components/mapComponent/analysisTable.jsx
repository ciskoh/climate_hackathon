import React, { useEffect, useState } from "react";

import { Box, DataTable, Meter, Text } from 'grommet';
import geojsonFile from '../../assets/test_aoi_valencia_subpolygon_but_json.json';
import test_aoi_subpolygon_with_metrics from '../../assets/test_aoi_subpolygon_with_metrics.json';
import { number } from 'prop-types';

let columns = [
  {
    property: 'fid',
    header: <Text>ID</Text>,
    sortable: true,
    size: 'xxsmall',

  },
  {
    property: 'DN',
    header: <Text>DN</Text>,
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
    property: 'soil_co2_estimates',
    header: 'Soil CO2 Estimates',
    sortable: true,
    size: 'medium',

    render: datum => (
      <Box pad={{ vertical: 'xsmall' }}>
        <Meter
          values={[{ value: datum.soil_co2_estimates }]}
          thickness="small"
          size="large"
        />
      </Box>
    ),
  },
  {
    property: 'vegetation_co2_estimates',
    header: 'vegetation_co2_estimates',
    sortable: true,
    size: 'medium',
    render: datum => (
      <Box pad={{ vertical: 'xsmall' }}>
        <Meter
          values={[{ value: datum.vegetation_co2_estimates }]}
          thickness="small"
          size="large"
        />
      </Box>
    ),
  },
]

const newGeojson = test_aoi_subpolygon_with_metrics;

const tempData = newGeojson;
const tempFeatures = tempData.features
const tableName = tempData.name

console.log(newGeojson);
const AnalysisTable = ({results}) => {
  const [ data, setData] = useState(geojsonFile)

  const tableName = geojsonFile.name

let polyColor = properties => {
  // console.log('from lopycolor function',properties);
  if (properties.land_cover === 'Cropland 1') return "gray"; 
  if (properties.land_cover === 'Cropland 2') return "yellow";
  if (properties.land_cover === 'Forest') return "darkgreen";
}






tempFeatures.forEach(feature =>{ 
  const tempFeature = {id: feature.properties.id, polygonName: feature.properties.land_cover, land_management: feature.properties.land_management, landCover: polyColor(feature.properties), soil_co2_estimates: feature.properties.soil_co2_estimates, vegetation_co2_estimates: feature.properties.vegetation_co2_estimates, coordinates: feature.geometry.coordinates[0]};
  // console.log(tempFeature.coordinates);
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
  useEffect(() => {
    let DATA = [];
    const tempFeatures = results.features
    tempFeatures.forEach(feature => 
      DATA.push(feature.properties)  
    )
    setData(DATA)
  }, [results])

  return (
    <Box align="center" pad="medium" height='100%'>
      <Text weight='bold'>{tableName}</Text>
      <DataTable 
        sortable 
        columns={columns} 
        data={data} 
        size="100%"
      />
    </Box>
  )
};

export default AnalysisTable;