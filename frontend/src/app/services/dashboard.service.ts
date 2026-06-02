import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private base = '/api/dashboard';

  constructor(private http: HttpClient) {}

  getSummary(windowMinutes: number = 5): Observable<any> {
    return this.http.get<any>(`${this.base}/summary?window_minutes=${windowMinutes}`);
  }

  getAnalytics(limit: number = 50) {
    return this.http.get<any[]>(`${this.base}/analytics?limit=${limit}`);
  }

  getAlerts(limit: number = 50) {
    return this.http.get<any[]>(`${this.base}/alerts?limit=${limit}`);
  }

  getDetections(limit: number = 50) {
    return this.http.get<any[]>(`${this.base}/detections?limit=${limit}`);
  }
}
