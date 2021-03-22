import React from 'react';


import { grommet, Grommet, Box, DataTable, Heading, Meter, Text } from 'grommet';

import { DATA } from './exampleData';

const columns = [
    {
      property: 'name',
      header: <Text>Name with extra</Text>,
      primary: true,
      footer: 'Total',
    },
    {
      property: 'location',
      header: 'Location',
    },
    {
      property: 'date',
      header: 'Date',
      render: datum =>
        datum.date && new Date(datum.date).toLocaleDateString('en-US'),
      align: 'end',
    },
    {
      property: 'percent',
      header: 'Percent Complete',
      render: datum => (
        <Box pad={{ vertical: 'xsmall' }}>
          <Meter
            values={[{ value: datum.percent }]}
            thickness="xsmall"
            size="small"
          />
        </Box>
      ),
    },
  ];

const ExampleDataTable = () => {

    return (
        <Grommet theme={ grommet }>
            <Box align="center" pad="large">
            <Heading level="3">Table for example</Heading>
            <DataTable
        columns={columns.map(column => ({ ...column,
            search: column.property === 'name' || column.property === 'location' }))}
            data={DATA}  
            sortable
            resizeable

        />
            </Box>
        </Grommet>
    )
}


export default ExampleDataTable;