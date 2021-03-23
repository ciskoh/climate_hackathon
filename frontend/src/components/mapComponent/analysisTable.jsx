import React from 'react';

import { Box, DataTable, Meter, Text } from 'grommet';


let columns = [
  {
    property: 'name',
    header: <Text>Use type</Text>,
  },
  {
    property: 'percent',
    header: 'Percens',
    render: datum => (
      <Box pad={{ vertical: 'xsmall' }}>
        <Meter
          values={[{ value: datum.percent }]}
          thickness="small"
          size="small"
        />
      </Box>
    ),
  },
]

let data=[
  {
    name: 'Built up',
    percent: 30,
  },
  {
    name: 'Fallow',
    percent: 40,
  },
  {
    name: 'Forrest',
    percent: 80,
  },
  {
    name: 'Crop 1',
    percent: 60,
  },
  {
    name: 'Crop 2',
    percent: 40,
  },
  {
    name: 'Crop 3',
    percent: 50,
  },

]


const AnalysisTable = () => (

      <Box align="center" pad="small">
        <DataTable 
          sortable 
          columns={columns} 
          data={data} 
          size="medium"
        />
      </Box>
);

export default AnalysisTable;