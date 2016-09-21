/**
 * Created by dido on 9/3/16.
 */
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './componenets/app.module';

const platform = platformBrowserDynamic();

platform.bootstrapModule(AppModule);
