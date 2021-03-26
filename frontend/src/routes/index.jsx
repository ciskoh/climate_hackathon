import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Redirect } from 'react-router-dom';
// ==================== pages ====================
import HomePage from '../pages/home';
import AboutPage from '../pages/about';
import AnalysisPage from '../pages/analysis';
import MapPage from '../pages/map';
// ===============================================


const Routes = () => {
    return <>
        <Router>
            <Switch>

                    <Route exact path='/' component={HomePage} />
                    <Route exact path='/map' component={MapPage} />
                    <Route exact path='/analysis' component={AnalysisPage} />
                    <Route exact path='/about' component={AboutPage} />
                    <Route render={() => <Redirect to={{pathname: '/'}} />} />

            </Switch>
        </Router>
    </>

};

export default Routes;