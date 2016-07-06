import { bootstrap }      from '@angular/platform-browser-dynamic';

import { AppComponent }   from './components/app.component';
import { APP_ROUTER_PROVIDERS } from './routes/app.routes';
import { HTTP_PROVIDERS } from '@angular/http';


//register the http services and router component at the bootstrap
// same effect of  providers[] array in @component decorator
bootstrap(AppComponent, [
    HTTP_PROVIDERS,
    APP_ROUTER_PROVIDERS
]);
