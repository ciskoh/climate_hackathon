import * as Constants from '../constants';
import data from '../../components/mapComponent/tempMapData/data.json';
import { options } from '../../components/mapComponent/tempMapData/options';

const initialState = {
    data,
    options,
    active: options[0]
  };
  
export const setActiveOptionReducer = (state = initialState, action) => {
  if (action.type === Constants.SET_ACTIVE_OPTION) {
    return {
      ...state,
        active: [...action.option]
    }
  } else {
      return state;
  }
};