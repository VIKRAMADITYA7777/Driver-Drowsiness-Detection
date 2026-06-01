import { Component, OnInit } from '@angular/core';

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

  ngOnInit(): void {
    this.metricCards = [
      { title: 'Fatigue Score', value: '18%', detail: 'Low risk', status: 'normal' },
      { title: 'Blink Rate', value: '14 / min', detail: 'Optimal', status: 'normal' },
      { title: 'PERCLOS', value: '3.8%', detail: 'Safe', status: 'normal' },
      { title: 'Drowsy Alerts', value: '1', detail: 'Recent warning', status: 'warning' }
    ];
  }
}
