// import thunk from "redux-thunk";
import { createStore } from "redux";
import { rootReducer } from "./reducers";



export const store = createStore(rootReducer);