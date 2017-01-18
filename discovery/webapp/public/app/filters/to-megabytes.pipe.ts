import { Pipe, PipeTransform } from '@angular/core';
/*
 * Usage:
 *   value | toMegabytes
 * Example:
 *   {{ 2 |  exponentialStrength}}
*/
@Pipe({name: 'toMegabytes'})
export class ToMegabytes implements PipeTransform {
  transform(numberInBytes: number): number {
    //let exp = parseFloat(exponent);
    return Math.round(numberInBytes/1000/1000);
  }
}
