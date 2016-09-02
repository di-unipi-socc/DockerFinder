/**
 * Created by dido on 7/6/16.
 */
import { provideRouter, RouterConfig }  from '@angular/router';
import { ImagesComponent }              from '../components/images.component';
import { DashboardComponent }           from '../components/dashboard.component'
import { ImageDetailComponent }         from "../components/image-detail.component";


export const routes: RouterConfig = [
      {
      path: '',
      redirectTo: '/dashboard',
      pathMatch: 'full'
    },
    {
        path: 'dashboard',
        component: DashboardComponent
    },
    {
        path: 'detail/:id',
        component: ImageDetailComponent
    },
    {
        path: 'images/:parm',  //addres bar url /images
        component: ImagesComponent
    }
];

export const APP_ROUTER_PROVIDERS = [
  provideRouter(routes)
];