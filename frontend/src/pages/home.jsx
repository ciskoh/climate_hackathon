import * as React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navi from '../components/navi';

import { Box, Stack } from 'grommet';

import LeafLetMap from '../components/mapComponent/drawOnMap';



const HomePage = () => {

  return (
    <>
      <Navi />

      <Box margin='small' flex direction='row' >
        <Stack anchor='center'>  
        <Box>
          <LeafLetMap />
        </Box>
        </Stack>
      </Box>
    </>
  )
}

export default HomePage;
