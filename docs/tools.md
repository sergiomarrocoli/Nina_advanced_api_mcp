# Tools

Every MCP tool the server exposes, grouped by device. **core** and **mono** show the proposed profiles
(see issue #3): `core` is connecting, guiding, cooling, slewing, focusing and capturing; `mono` is `core` plus the filter wheel.
Tools marked **harness** are not in this server: the benchmark harness adds them (`nina_autofocus`, `nina_center_mount`, and a capped `nina_wait`), and issue #5 moves them here.

104 tools in the server.

| Tool | Profile |
|---|---|
| **Connection and status** | |
| `nina_connect` | core |
| `nina_disconnect` | core |
| `nina_get_status` | core |
| `nina_get_version` |  |
| `nina_get_plugins` |  |
| `nina_time_now` |  |
| `nina_help` |  |
| `nina_switch_tab` |  |
| `nina_get_screenshot` |  |
| **Camera** | |
| `nina_connect_camera` | core |
| `nina_disconnect_camera` | core |
| `nina_list_camera_devices` |  |
| `nina_get_camera_info` | core |
| `nina_capture_image` | core |
| `nina_abort_exposure` | core |
| `nina_get_capture_statistics` |  |
| `nina_start_cooling` | core |
| `nina_stop_cooling` | core |
| `nina_start_warming` | core |
| `nina_set_binning` |  |
| `nina_set_readout_mode` |  |
| **Images** | |
| `nina_get_image` | core |
| `nina_get_image_history` |  |
| `nina_get_image_thumbnail` |  |
| `nina_get_image_parameter` |  |
| `nina_get_image_parameters` |  |
| `nina_set_image_parameter` |  |
| `nina_reset_image_parameters` |  |
| **Mount** | |
| `nina_connect_mount` | core |
| `nina_disconnect_mount` | core |
| `nina_list_mount_devices` |  |
| `nina_rescan_mount_devices` |  |
| `nina_get_mount_info` | core |
| `nina_slew_mount` | core |
| `nina_stop_slew` | core |
| `nina_sync_mount` | core |
| `nina_flip_mount` |  |
| `nina_park_mount` | core |
| `nina_unpark_mount` | core |
| `nina_home_mount` |  |
| `nina_set_park_position` |  |
| `nina_set_tracking_mode` |  |
| **Focuser** | |
| `nina_connect_focuser` | core |
| `nina_disconnect_focuser` | core |
| `nina_list_focuser_devices` |  |
| `nina_rescan_focuser_devices` |  |
| `nina_get_focuser_info` | core |
| `nina_move_focuser` | core |
| `nina_set_focuser_temperature` |  |
| **Filter wheel** | |
| `nina_connect_filterwheel` | core |
| `nina_disconnect_filterwheel` | core |
| `nina_list_filterwheel_devices` |  |
| `nina_rescan_filterwheel_devices` |  |
| `nina_get_filterwheel_info` | mono |
| `nina_get_filter_info` | mono |
| `nina_change_filter` | mono |
| **Guider (PHD2)** | |
| `nina_connect_guider` | core |
| `nina_disconnect_guider` | core |
| `nina_list_guider_devices` |  |
| `nina_rescan_guider_devices` |  |
| `nina_get_guider_info` | core |
| `nina_start_guiding` | core |
| `nina_stop_guiding` | core |
| `nina_calibrate_guider` | core |
| `nina_clear_guider_calibration` | core |
| `nina_get_guider_graph` | core |
| **Rotator** | |
| `nina_connect_rotator` |  |
| `nina_disconnect_rotator` |  |
| `nina_list_rotator_devices` |  |
| `nina_rescan_rotator_devices` |  |
| `nina_get_rotator_info` |  |
| `nina_move_rotator` |  |
| `nina_halt_rotator` |  |
| `nina_sync_rotator` |  |
| `nina_set_rotator_reverse` |  |
| **Flat panel and flats** | |
| `nina_connect_flatpanel` |  |
| `nina_disconnect_flatpanel` |  |
| `nina_list_flatpanel_devices` |  |
| `nina_rescan_flatpanel_devices` |  |
| `nina_get_flatpanel_info` |  |
| `nina_set_flatpanel_brightness` |  |
| `nina_set_flatpanel_cover` |  |
| `nina_set_flatpanel_light` |  |
| `nina_start_flats` |  |
| `nina_stop_flats` |  |
| `nina_sky_flats` |  |
| `nina_get_flats_status` |  |
| `nina_get_flats_progress` |  |
| **Dome** | |
| `nina_connect_dome` |  |
| `nina_disconnect_dome` |  |
| `nina_list_dome_devices` |  |
| `nina_rescan_dome_devices` |  |
| `nina_get_dome_info` |  |
| `nina_slew_dome` |  |
| `nina_park_dome` |  |
| `nina_home_dome` |  |
| `nina_stop_dome_movement` |  |
| `nina_open_dome_shutter` |  |
| `nina_close_dome_shutter` |  |
| `nina_set_dome_follow` |  |
| `nina_sync_dome_to_telescope` |  |
| `nina_set_dome_park_position` |  |
| **Other** | |
| `nina_control_dew_heater` |  |
| `nina_wait` |  |
| **Added by the benchmark harness** | |
| `nina_autofocus` | core (harness) |
| `nina_center_mount` | core (harness) |
