import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../services/dashboard.service';

interface MetricCard {
  title: string;
  value: string;
  detail: string;
  status: 'normal' | 'warning' | 'critical';
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  metricCards: MetricCard[] = [];

  constructor(private ds: DashboardService) {}

  ngOnInit(): void {
    this.metricCards = [
      { title: 'Fatigue Score', value: '-', detail: '-', status: 'normal' },
      { title: 'Blink Rate', value: '-', detail: '-', status: 'normal' },
      { title: 'PERCLOS', value: '-', detail: '-', status: 'normal' },
      { title: 'Drowsy Alerts', value: '-', detail: '-', status: 'normal' }
    ];

    this.ds.getSummary(5).subscribe(summary => {
      this.metricCards[0].value = `${(summary.avg_perclos * 100).toFixed(1)}%`;
      this.metricCards[1].value = `${summary.detections}`;
      this.metricCards[2].value = `${(summary.avg_perclos * 100).toFixed(1)}%`;
      this.metricCards[3].value = `${summary.alerts}`;
      if (summary.alerts > 0) this.metricCards[3].status = 'warning';
    });
  }
}
