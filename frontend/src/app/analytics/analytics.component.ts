import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../services/dashboard.service';

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.scss']
})
export class AnalyticsComponent implements OnInit {
  analytics: any[] = [];

  constructor(private ds: DashboardService) {}

  ngOnInit(): void {
    this.ds.getAnalytics(20).subscribe(a => this.analytics = a || []);
  }
}
