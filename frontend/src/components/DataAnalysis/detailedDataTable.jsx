import React from "react";

import { Box, DataTable, Meter, Text } from 'grommet';
import test_aoi_subpolygon_with_metrics from '../../assets/test_aoi_subpolygon_with_metrics.json';


let columns = [
  {
    property: 'id',
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
    header: <Text>Management Type</Text>,
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

let DATA = [];
tempFeatures.forEach(feature =>{ 
    const tempFeature = { id: feature.properties.fid, DN: feature.properties.DN,  land_management: feature.properties.land_management, land_cover: feature.properties.land_cover, 
        soil_co2_estimates: feature.properties.soil_co2_estimates, vegetation_co2_estimates: feature.properties.vegetation_co2_estimates, coordinates: feature.geometry.coordinates[0]
    };
  DATA.push(tempFeature)  
});



const DetailedDataTable = () => {

    return (
        <>
            <Box align="center" pad="medium" height='100%'>
            <Text weight='bold'>{tableName}</Text>
            <DataTable 
                sortable 
                columns={columns} 
                data={DATA} 
                size="100%"
            />
            </Box>
        </>
    )
}

export default DetailedDataTable;