import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Redirect } from 'react-router-dom';
// ==================== pages ====================
import HomePage from '../pages/home';
import SciencePage from '../pages/science';
import AboutPage from '../pages/about';
// ===============================================


const Routes = () => {
    return <>
        <Router>
            <Switch>

                    <Route exact path='/' component={HomePage} />
                    <Route exact path='/science' component={SciencePage} />
                    <Route exact path='/about' component={AboutPage} />
                    <Route render={() => <Redirect to={{pathname: '/'}} />} />

            </Switch>
        </Router>
    </>

};

export default Routes;