"use strict";
/**
 * Created by dido on 7/6/16.
 */
var router_1 = require('@angular/router');
var images_component_1 = require('../components/images.component');
var dashboard_component_1 = require('../components/dashboard.component');
var image_detail_component_1 = require("../components/image-detail.component");
exports.routes = [
    {
        path: '',
        redirectTo: '/dashboard',
        pathMatch: 'full'
    },
    {
        path: 'dashboard',
        component: dashboard_component_1.DashboardComponent
    },
    {
        path: 'detail/:id',
        component: image_detail_component_1.ImageDetailComponent
    },
    {
        path: 'images',
        component: images_component_1.ImagesComponent
    }
];
exports.APP_ROUTER_PROVIDERS = [
    router_1.provideRouter(exports.routes)
];
//# sourceMappingURL=app.routes.js.map