using NetDaemon.Common;

namespace Netdaemon.Generated.Extensions
{
    public static partial class EntityExtension
    {
        public static SwitchEntities SwitchEx(this NetDaemonApp app) => new SwitchEntities(app);
        public static LightEntities LightEx(this NetDaemonApp app) => new LightEntities(app);
        public static MediaPlayerEntities MediaPlayerEx(this NetDaemonApp app) => new MediaPlayerEntities(app);
        public static ScriptEntities ScriptEx(this NetDaemonApp app) => new ScriptEntities(app);
        public static SceneEntities SceneEx(this NetDaemonApp app) => new SceneEntities(app);
        public static CameraEntities CameraEx(this NetDaemonApp app) => new CameraEntities(app);
        public static AutomationEntities AutomationEx(this NetDaemonApp app) => new AutomationEntities(app);
    }

    public partial class SwitchEntities
    {
        private readonly NetDaemonApp _app;
        public SwitchEntities(NetDaemonApp app)
        {
            _app = app;
        }

        public IEntity Remote1B1 => _app.Entity("switch.remote_1_b1");
        public IEntity Film => _app.Entity("switch.film");
        public IEntity TvrumVagg => _app.Entity("switch.tvrum_vagg");
        public IEntity JulbelysningKokV => _app.Entity("switch.julbelysning_kok_v");
        public IEntity Switch7 => _app.Entity("switch.switch7");
        public IEntity Switch8MelkersTv => _app.Entity("switch.switch8_melkers_tv");
        public IEntity NetdaemonMotion => _app.Entity("switch.netdaemon_motion");
        public IEntity Switch1Rb => _app.Entity("switch.switch_1_rb");
        public IEntity NetdaemonRoomSpecific => _app.Entity("switch.netdaemon_room_specific");
        public IEntity Motorvarmare => _app.Entity("switch.motorvarmare");
        public IEntity Switch15 => _app.Entity("switch.switch15");
        public IEntity SallysRumFonster => _app.Entity("switch.sallys_rum_fonster");
        public IEntity Switch1 => _app.Entity("switch.switch1");
        public IEntity Remote1B2 => _app.Entity("switch.remote_1_b2");
        public IEntity Switch14 => _app.Entity("switch.switch14");
        public IEntity Switch1Lb => _app.Entity("switch.switch_1_lb");
        public IEntity Switch5MelkersFan => _app.Entity("switch.switch5_melkers_fan");
        public IEntity Switch12 => _app.Entity("switch.switch12");
        public IEntity Switch4TomasFan => _app.Entity("switch.switch4_tomas_fan");
        public IEntity Remote1B3 => _app.Entity("switch.remote_1_b3");
        public IEntity Switch10 => _app.Entity("switch.switch10");
        public IEntity ADiod => _app.Entity("switch.a_diod");
        public IEntity Switch66 => _app.Entity("switch.switch66");
        public IEntity NetdaemonHouseStateManager => _app.Entity("switch.netdaemon_house_state_manager");
        public IEntity NetdaemonGlobalApp => _app.Entity("switch.netdaemon_global_app");
        public IEntity JulbelysningVardagsrumV => _app.Entity("switch.julbelysning_vardagsrum_v");
        public IEntity Sonoff1Relay => _app.Entity("switch.sonoff1_relay");
        public IEntity NetdaemonLightManager => _app.Entity("switch.netdaemon_light_manager");
        public IEntity MelkersRumFonster => _app.Entity("switch.melkers_rum_fonster");
        public IEntity Tv => _app.Entity("switch.tv");
        public IEntity Testswitch => _app.Entity("switch.testswitch");
        public IEntity NetdaemonHacsNotifyOnUpdate => _app.Entity("switch.netdaemon_hacs_notify_on_update");
        public IEntity KokKaffebryggare => _app.Entity("switch.kok_kaffebryggare");
        public IEntity JulbelysningKokH => _app.Entity("switch.julbelysning_kok_h");
        public IEntity NetdaemonTv => _app.Entity("switch.netdaemon_tv");
        public IEntity Switch13 => _app.Entity("switch.switch13");
        public IEntity JulbelysningVardagsrumH => _app.Entity("switch.julbelysning_vardagsrum_h");
        public IEntity NetdaemonMyApp => _app.Entity("switch.netdaemon_my_app");
        public IEntity Switch2 => _app.Entity("switch.switch2");
        public IEntity ShellyRelay => _app.Entity("switch.shelly_relay");
        public IEntity Switch3 => _app.Entity("switch.switch3");
        public IEntity NetdaemonCalendarTrash => _app.Entity("switch.netdaemon_calendar_trash");
        public IEntity JulbelysningVardagsrumM => _app.Entity("switch.julbelysning_vardagsrum_m");
        public IEntity ComputerTomas => _app.Entity("switch.computer_tomas");
        public IEntity NetdaemonMotorvarmare => _app.Entity("switch.netdaemon_motorvarmare");
        public IEntity NetdaemonWelcomeHome => _app.Entity("switch.netdaemon_welcome_home");
        public IEntity JulbelysningTomasRum => _app.Entity("switch.julbelysning_tomas_rum");
        public IEntity Switch9outdoor => _app.Entity("switch.switch9outdoor");
        public IEntity Switch16 => _app.Entity("switch.switch16");
        public IEntity JulbelysningSovrum => _app.Entity("switch.julbelysning_sovrum");
        public IEntity Switch11 => _app.Entity("switch.switch11");
        public IEntity NetdaemonMagicCube => _app.Entity("switch.netdaemon_magic_cube");
    }

    public partial class LightEntities
    {
        private readonly NetDaemonApp _app;
        public LightEntities(NetDaemonApp app)
        {
            _app = app;
        }

        public IEntity Farstukvisten => _app.Entity("light.farstukvisten");
        public IEntity TvrumVagg => _app.Entity("light.tvrum_vagg");
        public IEntity HallDorr => _app.Entity("light.hall_dorr");
        public IEntity SallysRumFonster => _app.Entity("light.sallys_rum_fonster");
        public IEntity Vardagsrum => _app.Entity("light.vardagsrum");
        public IEntity JulbelysningSovrum => _app.Entity("light.julbelysning_sovrum");
        public IEntity SovrumFonster => _app.Entity("light.sovrum_fonster");
        public IEntity VardagsrumFonsterMitten => _app.Entity("light.vardagsrum_fonster_mitten");
        public IEntity MelkersRum => _app.Entity("light.melkers_rum");
        public IEntity JulbelysningTomasRum => _app.Entity("light.julbelysning_tomas_rum");
        public IEntity TvrumFonsterVanster => _app.Entity("light.tvrum_fonster_vanster");
        public IEntity SovrumBrya => _app.Entity("light.sovrum_brya");
        public IEntity JulbelysningKokH => _app.Entity("light.julbelysning_kok_h");
        public IEntity VardagsrumFonsterHoger => _app.Entity("light.vardagsrum_fonster_hoger");
        public IEntity SallysRum => _app.Entity("light.sallys_rum");
        public IEntity KokFonster => _app.Entity("light.kok_fonster");
        public IEntity TvrumBakgrundTv => _app.Entity("light.tvrum_bakgrund_tv");
        public IEntity JulbelysningKokV => _app.Entity("light.julbelysning_kok_v");
        public IEntity TomasRum => _app.Entity("light.tomas_rum");
        public IEntity Sovrum => _app.Entity("light.sovrum");
        public IEntity TomasRumFonster => _app.Entity("light.tomas_rum_fonster");
        public IEntity ConfigurationTool27 => _app.Entity("light.configuration_tool_27");
        public IEntity Kok => _app.Entity("light.kok");
        public IEntity FarstukvistLed => _app.Entity("light.farstukvist_led");
        public IEntity VardagsrumFonsterVanster => _app.Entity("light.vardagsrum_fonster_vanster");
        public IEntity HallByra => _app.Entity("light.hall_byra");
        public IEntity JulbelysningVardagsrumV => _app.Entity("light.julbelysning_vardagsrum_v");
        public IEntity MelkersRumFonster => _app.Entity("light.melkers_rum_fonster");
        public IEntity KokLillaFonster => _app.Entity("light.kok_lilla_fonster");
        public IEntity JulbelysningVardagsrumH => _app.Entity("light.julbelysning_vardagsrum_h");
        public IEntity Ambient => _app.Entity("light.ambient");
        public IEntity JulbelysningVardagsrumM => _app.Entity("light.julbelysning_vardagsrum_m");
        public IEntity TvrumFonsterHoger => _app.Entity("light.tvrum_fonster_hoger");
        public IEntity Tvrummet => _app.Entity("light.tvrummet");
    }

    public partial class MediaPlayerEntities
    {
        private readonly NetDaemonApp _app;
        public MediaPlayerEntities(NetDaemonApp app)
        {
            _app = app;
        }

        public IMediaPlayer PlexKodiAddOnLibreelec => _app.MediaPlayer("media_player.plex_kodi_add_on_libreelec");
        public IMediaPlayer PlexChromecast => _app.MediaPlayer("media_player.plex_chromecast");
        public IMediaPlayer PlexPlexWebChrome => _app.MediaPlayer("media_player.plex_plex_web_chrome");
        public IMediaPlayer MelkersTv => _app.MediaPlayer("media_player.melkers_tv");
        public IMediaPlayer SallysHogtalare => _app.MediaPlayer("media_player.sallys_hogtalare");
        public IMediaPlayer MelkersRum => _app.MediaPlayer("media_player.melkers_rum");
        public IMediaPlayer TvUppe2 => _app.MediaPlayer("media_player.tv_uppe2");
        public IMediaPlayer PlexChrome2 => _app.MediaPlayer("media_player.plex_chrome_2");
        public IMediaPlayer PlexChrome => _app.MediaPlayer("media_player.plex_chrome");
        public IMediaPlayer KodiTvNere => _app.MediaPlayer("media_player.kodi_tv_nere");
        public IMediaPlayer Kok => _app.MediaPlayer("media_player.kok");
        public IMediaPlayer Vardagsrum => _app.MediaPlayer("media_player.vardagsrum");
        public IMediaPlayer Huset => _app.MediaPlayer("media_player.huset");
        public IMediaPlayer PlexTomasIpad => _app.MediaPlayer("media_player.plex_tomas_ipad");
        public IMediaPlayer TvRummetGh => _app.MediaPlayer("media_player.tv_rummet_gh");
        public IMediaPlayer Sovrum => _app.MediaPlayer("media_player.sovrum");
        public IMediaPlayer TvUppe => _app.MediaPlayer("media_player.tv_uppe");
        public IMediaPlayer PlexChrome3 => _app.MediaPlayer("media_player.plex_chrome_3");
        public IMediaPlayer TvNere => _app.MediaPlayer("media_player.tv_nere");
    }

    public partial class ScriptEntities
    {
        private readonly NetDaemonApp _app;
        public ScriptEntities(NetDaemonApp app)
        {
            _app = app;
        }

        public IEntity CleaningScene => _app.Entity("script.cleaning_scene");
        public IEntity MorningScene => _app.Entity("script.morning_scene");
        public IEntity Setnightmode => _app.Entity("script.setnightmode");
        public IEntity ColorScene => _app.Entity("script.color_scene");
        public IEntity DayScene => _app.Entity("script.day_scene");
        public IEntity NotifyGreet => _app.Entity("script.notify_greet");
        public IEntity EveningScene => _app.Entity("script.evening_scene");
        public IEntity TvScene => _app.Entity("script.tv_scene");
        public IEntity Notify => _app.Entity("script.notify");
        public IEntity FilmScene => _app.Entity("script.film_scene");
        public IEntity NightScene => _app.Entity("script.night_scene");
        public IEntity TvOffScene => _app.Entity("script.tv_off_scene");
        public IEntity E1586350051032 => _app.Entity("script.1586350051032");
    }

    public partial class SceneEntities
    {
        private readonly NetDaemonApp _app;
        public SceneEntities(NetDaemonApp app)
        {
            _app = app;
        }

        public IEntity Morgon => _app.Entity("scene.morgon");
        public IEntity Stadning => _app.Entity("scene.stadning");
        public IEntity Natt => _app.Entity("scene.natt");
        public IEntity Kvall => _app.Entity("scene.kvall");
        public IEntity Dag => _app.Entity("scene.dag");
    }

    public partial class CameraEntities
    {
        private readonly NetDaemonApp _app;
        public CameraEntities(NetDaemonApp app)
        {
            _app = app;
        }

        public ICamera Kamera3 => _app.Camera("camera.kamera_3");
        public ICamera MyCamera => _app.Camera("camera.my_camera");
        public ICamera KameraStream => _app.Camera("camera.kamera_stream");
    }

    public partial class AutomationEntities
    {
        private readonly NetDaemonApp _app;
        public AutomationEntities(NetDaemonApp app)
        {
            _app = app;
        }

        public IEntity SetThemeAtStartup => _app.Entity("automation.set_theme_at_startup");
    }
}