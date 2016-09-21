"use strict";
var router_1 = require('@angular/router');
var dashboard_component_1 = require("../componenets/dashboard.component");
var images_component_1 = require("../componenets/images.component");
//import { DashboardComponent }           from '../components/dashboard.component'
//import { ImageDetailComponent }         from "../components/image-detail.component";
exports.appRoutes = [
    {
        path: '',
        redirectTo: '/dashboard',
        pathMatch: 'full'
    },
    {
        path: 'dashboard',
        component: dashboard_component_1.DashboardComponent
    },
    // {
    //     path: 'detail/:id',
    //     component: ImageDetailComponent
    // },
    {
        path: 'images/:parm',
        component: images_component_1.ImagesComponent
    }
];
exports.routing = router_1.RouterModule.forRoot(exports.appRoutes);
// export const APP_ROUTER_PROVIDERS = [
//   provideRouter(routes)
// ]; 
//# sourceMappingURL=app.routes.js.map