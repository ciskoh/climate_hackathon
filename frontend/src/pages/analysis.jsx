import * as React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navi from '../components/navi';

import { Box } from 'grommet';
import DetailedDataTable from '../components/DataAnalysis/detailedDataTable';



const AnalysisPage = () => {

  return (
    <>
      <Navi />
      <Box width="95vw" height="2xl" margin='medium' pad='medium' alignSelf='center' direction='coulmn' >
      <Box elevation='medium' width='2xl' height='100%' border>
          <DetailedDataTable />
        </Box>
        <Box align='end' justify='center' margin='medium'>
        </Box>
      </Box>
    </>
  )
}

export default AnalysisPage;
