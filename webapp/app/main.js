"use strict";
var platform_browser_dynamic_1 = require('@angular/platform-browser-dynamic');
var app_component_1 = require('./components/app.component');
var app_routes_1 = require('./routes/app.routes');
var http_1 = require('@angular/http');
//register the http services and router component at the bootstrap
// same effect of  providers[] array in @component decorator
platform_browser_dynamic_1.bootstrap(app_component_1.AppComponent, [
    http_1.HTTP_PROVIDERS,
    app_routes_1.APP_ROUTER_PROVIDERS
]);
//# sourceMappingURL=main.js.map