import * as Constants from '../constants';


const initialState = {

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