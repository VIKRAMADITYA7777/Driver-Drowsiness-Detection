import { Component } from '@angular/core';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  menuItems = [
    { icon: 'dashboard', label: 'Dashboard' },
    { icon: 'insights', label: 'Analytics' },
    { icon: 'settings', label: 'System' },
    { icon: 'history', label: 'History' }
  ];
}
