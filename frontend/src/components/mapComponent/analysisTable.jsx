import React, { useEffect, useState } from "react";

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



const AnalysisTable = ({results}) => {
  const [ data, setData] = useState(geojsonFile)

  const tableName = geojsonFile.name


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