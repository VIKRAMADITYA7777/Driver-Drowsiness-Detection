import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from './material.module';
import { HttpClientModule } from '@angular/common/http';
import { AlertsComponent } from './alerts/alerts.component';
import { AnalyticsComponent } from './analytics/analytics.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { VisualThreeComponent } from './visual-three/visual-three.component';

@NgModule({
  declarations: [AppComponent, DashboardComponent, SidebarComponent, VisualThreeComponent, AlertsComponent, AnalyticsComponent],
  imports: [BrowserModule, BrowserAnimationsModule, MaterialModule, AppRoutingModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
