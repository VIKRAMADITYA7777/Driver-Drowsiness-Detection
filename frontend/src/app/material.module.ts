import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatGridListModule } from '@angular/material/grid-list';

@NgModule({
  exports: [
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatListModule,
    MatSidenavModule,
    MatTooltipModule,
    MatGridListModule
  ]
})
export class MaterialModule {}
