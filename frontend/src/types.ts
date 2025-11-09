export type Alert = {
  id: string;
  type: string;
  message: string;
  level: 'info' | 'warning' | 'critical';
  timestamp: string;
};

export type Calibration = {
  id: string;
  device_id: string;
  offset: number;
  note?: string;
  timestamp: string;
};

export type WeeklyReport = {
  week: string;
  totals: {
    menu_items: number;
    calibrations: number;
    alerts: number;
  };
  notes: string[];
};
