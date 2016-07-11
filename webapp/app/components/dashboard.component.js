"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
/**
 * Created by dido on 7/6/16.
 */
var core_1 = require('@angular/core');
var router_1 = require('@angular/router');
var image_service_1 = require('../services/image.service');
var images_search_component_1 = require('./images-search.component');
var DashboardComponent = (function () {
    function DashboardComponent(imageService, router) {
        this.imageService = imageService;
        this.router = router;
        this.images = [];
    }
    DashboardComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.imageService.getImages()
            .then(function (images) { return _this.images = images.slice(1, 5); });
    };
    DashboardComponent.prototype.gotoDetail = function (image) {
        var link = ['/detail', image._id];
        this.router.navigate(link);
    };
    DashboardComponent = __decorate([
        core_1.Component({
            selector: 'my-dashboard',
            templateUrl: 'app/template/dashboard.component.html',
            styleUrls: ["app/styles/dashboard.component.css"],
            directives: [images_search_component_1.ImagesSearchComponent]
        }), 
        __metadata('design:paramtypes', [image_service_1.ImageService, router_1.Router])
    ], DashboardComponent);
    return DashboardComponent;
}());
exports.DashboardComponent = DashboardComponent;
//# sourceMappingURL=dashboard.component.js.map