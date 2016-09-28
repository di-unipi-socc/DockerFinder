
/**
 * Created by dido on 7/6/16.
 */
//import { provideRouter, RouterConfig }  from '@angular/router';
import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


import {DashboardComponent}     from "../componenets/dashboard.component";
import {ImagesComponent}        from "../componenets/images.component";
//import { DashboardComponent }           from '../components/dashboard.component'
//import { ImageDetailComponent }         from "../components/image-detail.component";



export const appRoutes: Routes = [
      {
      path: '',
      redirectTo: '/dockerfinder',
      pathMatch: 'full'
    },
    {
        path: 'dockerfinder',
        component: DashboardComponent
    },
    // {
    //     path: 'detail/:id',
    //     component: ImageDetailComponent
    // },
    {
        path: 'images/:parm',  //addres bar url /images
        component: ImagesComponent
    }
];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);

// export const APP_ROUTER_PROVIDERS = [
//   provideRouter(routes)
// ];