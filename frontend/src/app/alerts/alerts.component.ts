import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../services/dashboard.service';

@Component({
  selector: 'app-alerts',
  templateUrl: './alerts.component.html',
  styleUrls: ['./alerts.component.scss']
})
export class AlertsComponent implements OnInit {
  alerts: any[] = [];

  constructor(private ds: DashboardService) {}

  ngOnInit(): void {
    this.ds.getAlerts(10).subscribe(a => this.alerts = a || []);
  }
}
