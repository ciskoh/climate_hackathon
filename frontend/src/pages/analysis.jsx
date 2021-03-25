import * as React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navi from '../components/navi';

import { Box, Stack } from 'grommet';

import LeafLetMap from '../components/mapComponent/drawOnMap';


const AnalysisPage = () => {

  return (
    <>
      <Navi />

      <Box margin='small' flex direction='row' >
        <Stack anchor='center'>  
        <Box 
          width="large" 
          height="large"
          border
          pad='xsmall'
        >
          {/* <LeafLetMap /> */}
        </Box>
        </Stack>
        <Box align='end' justify='center' margin='medium'>


        </Box>
      </Box>
    </>
  )
}

export default AnalysisPage;
