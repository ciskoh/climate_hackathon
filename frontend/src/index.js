import React from 'react';
import ReactDOM from 'react-dom';

import { store } from "./store";
import { Provider } from 'react-redux';

import Routes from "./routes";

import './index.css';
import { grommet, Grommet } from 'grommet';


ReactDOM.render(
  <React.StrictMode>
     <Provider store={store}>
     <Grommet theme={ grommet }>
            <Routes />
     </Grommet>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);
