import { store } from '../';
import * as Constants from '../constants';

export const setActiveOption = (option) => {
  store.dispatch({
    type: Constants.SET_ACTIVE_OPTION,
    option
  });
}