import { bootstrap }      from '@angular/platform-browser-dynamic';
import { disableDeprecatedForms, provideForms } from '@angular/forms';

import { AppComponent }   from './components/app.component';
import { APP_ROUTER_PROVIDERS } from './routes/app.routes';
import { HTTP_PROVIDERS } from '@angular/http';


//register the http services and router component at the bootstrap
// same effect of  providers[] array in @component decorator
bootstrap(AppComponent, [
    HTTP_PROVIDERS,
    APP_ROUTER_PROVIDERS,
    disableDeprecatedForms(),  //disable old api form and warning in the browser
    provideForms()
]).catch((err: any) => console.error(err));
