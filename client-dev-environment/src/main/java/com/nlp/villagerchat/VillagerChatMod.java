// Paketdefinition für die Mod
package com.nlp.villagerchat;
import com.mojang.logging.LogUtils;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraft.client.Minecraft;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.npc.Villager;
import net.minecraft.world.entity.npc.VillagerData;
import net.minecraft.world.item.*;
import net.minecraft.world.item.trading.MerchantOffer;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.phys.AABB;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.event.RegisterCommandsEvent;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.server.ServerStartingEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.event.lifecycle.FMLClientSetupEvent;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import org.slf4j.Logger;
import net.minecraft.core.registries.BuiltInRegistries;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.*;
import java.util.concurrent.CompletableFuture;

import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.server.level.ServerLevel;


// Die Hauptklasse des Mods, identifiziert durch die @Mod-Annotation
@Mod(VillagerChatMod.MODID)
public class VillagerChatMod {
    // Die Mod-ID
    public static final String MODID = "villagerchat";
    // Logger zur Konsolenausgabe
    private static final Logger LOGGER = LogUtils.getLogger();

    // Registrierung von Blöcken, Items und kreativen Tabs über DeferredRegister
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, MODID);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, MODID);
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    // Beispielblock mit Eigenschaften wie Steinfarbe
    public static final RegistryObject<Block> EXAMPLE_BLOCK = BLOCKS.register("example_block",
            () -> new Block(BlockBehaviour.Properties.of()
                    .setId(BLOCKS.key("example_block"))
                    .mapColor(MapColor.STONE)
            )
    );

    // BlockItem-Variante für den obigen Block
    public static final RegistryObject<Item> EXAMPLE_BLOCK_ITEM = ITEMS.register("example_block",
            () -> new BlockItem(EXAMPLE_BLOCK.get(), new Item.Properties().setId(ITEMS.key("example_block")))
    );

    // Einfaches Item, das essbar ist
    public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item",
            () -> new Item(new Item.Properties()
                    .setId(ITEMS.key("example_item"))
                    .food(new net.minecraft.world.food.FoodProperties.Builder()
                            .alwaysEdible()
                            .nutrition(1)
                            .saturationModifier(2f)
                            .build()
                    )
            )
    );

    // Ein eigener Reiter im Kreativmodus, in dem das Beispielitem auftaucht
    public static final RegistryObject<CreativeModeTab> EXAMPLE_TAB = CREATIVE_MODE_TABS.register("example_tab", () -> CreativeModeTab.builder()
            .withTabsBefore(CreativeModeTabs.COMBAT)
            .icon(() -> EXAMPLE_ITEM.get().getDefaultInstance())
            .displayItems((parameters, output) -> {
                output.accept(EXAMPLE_ITEM.get());
            }).build());

    // Konstruktor der Hauptklasse – wird beim Laden des Mods aufgerufen
    public VillagerChatMod(FMLJavaModLoadingContext context) {
        IEventBus modEventBus = context.getModEventBus();

        // Registrierung der Setup-Methode
        modEventBus.addListener(this::commonSetup);
        // Registrierung von Items, Blöcken und Tabs im EventBus
        BLOCKS.register(modEventBus);
        ITEMS.register(modEventBus);
        CREATIVE_MODE_TABS.register(modEventBus);
        modEventBus.addListener(this::addCreative);
        // Konfigurationsdatei registrieren
        context.registerConfig(ModConfig.Type.COMMON, Config.SPEC);

        // Registrierung am allgemeinen EventBus (z.B. für Ticks und Server-Events)
        MinecraftForge.EVENT_BUS.register(this);
    }

    // Wird einmal beim Initialisieren des Mods aufgerufen
    private void commonSetup(final FMLCommonSetupEvent event) {
        LOGGER.info("HELLO FROM COMMON SETUP");

        if (Config.logDirtBlock)
            LOGGER.info("DIRT BLOCK >> {}", ForgeRegistries.BLOCKS.getKey(Blocks.DIRT));

        LOGGER.info(Config.magicNumberIntroduction + Config.magicNumber);
        Config.items.forEach((item) -> LOGGER.info("ITEM >> {}", item.toString()));
    }

    // Fügt Items in bestimmte Kreativtabs ein
    private void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.BUILDING_BLOCKS)
            event.accept(EXAMPLE_BLOCK_ITEM);
    }

    // Wird beim Starten des Servers aufgerufen
    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event) {
        LOGGER.info("Server started");
    }

    // Registrierung eines Slash-Commands "/chat <message>"
    @SubscribeEvent
    public void onRegisterCommands(RegisterCommandsEvent event) {
        event.getDispatcher().register(
                Commands.literal("chat")
                        .then(Commands.argument("message", StringArgumentType.greedyString())
                                .executes(this::sendCustomMessage))
        );
    }

    // Hilfsklasse für das "Hinsehen"-Verhalten des Dorfbewohners
    private static class LookTask {
        public final Villager villager;
        public final LivingEntity target;
        public int ticksLeft;

        public LookTask(Villager villager, LivingEntity target, int ticks) {
            this.villager = villager;
            this.target = target;
            this.ticksLeft = ticks;
        }
    }

    // Aufgabenliste für das „Hinschauen“ von Dorfbewohnern
    private static final Map<Integer, LookTask> lookTasks = new HashMap<>();
    private static int taskIdCounter = 0;

    // Wird bei jedem Server-Tick aufgerufen, verarbeitet "LookTask"-Aufgaben
    @SubscribeEvent
    public void onServerTick(TickEvent.ServerTickEvent event) {
        if (event.phase == TickEvent.Phase.START) return;

        lookTasks.entrySet().removeIf(entry -> {
            LookTask task = entry.getValue();
            if (task.villager.isAlive() && task.target.isAlive()) {
                task.villager.getLookControl().setLookAt(task.target);
            }
            task.ticksLeft--;
            return task.ticksLeft <= 0;
        });
    }

    // Der zentrale Befehl: verarbeitet den Chatbefehl "/chat <message>"
    private int sendCustomMessage(CommandContext<CommandSourceStack> context) {
        String message = StringArgumentType.getString(context, "message");
        Entity sender = context.getSource().getEntity();

        // Fehler, falls kein Absender existiert
        if (sender == null || sender.level() == null) {
            context.getSource().sendFailure(Component.literal("Could not identify sender."));
            return 0;
        }

        // Nachricht an Spieler zurücksenden
        context.getSource().sendSuccess(() -> Component.literal("Du: " + message), false);

        // Sucht nach dem nächstgelegenen Dorfbewohner im Umkreis von 10 Blöcken
        AABB searchBox = new AABB(
                sender.getX() - 10, sender.getY() - 10, sender.getZ() - 10,
                sender.getX() + 10, sender.getY() + 10, sender.getZ() + 10
        );

        List<Villager> nearbyVillagers = sender.level().getEntitiesOfClass(Villager.class, searchBox);
        Villager closestVillager = null;
        double closestDist = Double.MAX_VALUE;

        for (Villager villager : nearbyVillagers) {
            double dist = villager.distanceToSqr(sender);
            if (dist < closestDist) {
                closestDist = dist;
                closestVillager = villager;
            }
        }

        if (closestVillager == null) {
            context.getSource().sendFailure(Component.literal("No nearby villager found."));
            return 0;
        }

        // Alle aktuellen Aktivitäten des Villagers abbrechen
        closestVillager.getBrain().stopAll((ServerLevel) closestVillager.level(), closestVillager);

        // Bewegung und Blickverhalten initialisieren
        if (sender instanceof LivingEntity livingSender) {
            PathNavigation navigation = closestVillager.getNavigation();
            navigation.moveTo(livingSender.getX(), livingSender.getY(), livingSender.getZ(), 0.7);
            closestVillager.getLookControl().setLookAt(livingSender);
            int taskId = taskIdCounter++;
            lookTasks.put(taskId, new LookTask(closestVillager, livingSender, 60));
        }

        // Asynchrone Verarbeitung der Nachricht (inkl. API-Call)
        Villager finalClosestVillager = closestVillager;
        CompletableFuture.runAsync(() -> {
            try {
                List<String> contextEntries = new ArrayList<>();

                // Kontextdaten des Villagers sammeln (Beruf, Level, etc.)
                VillagerData data = finalClosestVillager.getVillagerData();
                int level = data.level();
                String levelName = switch (level) {
                    case 1 -> "Anfänger";
                    case 2 -> "Lehrling";
                    case 3 -> "Geselle";
                    case 4 -> "Experte";
                    case 5 -> "Meister";
                    default -> "Unbekannt";
                };
                contextEntries.add("villager_level: " + levelName);

                String professionKey = BuiltInRegistries.VILLAGER_PROFESSION.getKey(data.profession().value()).getPath();
                contextEntries.add("villager_profession: " + professionKey);

                // Distanz zum Spieler
                double distance = Math.sqrt(finalClosestVillager.distanceToSqr(sender));
                contextEntries.add("villager_distance_to_player: " + String.format("%.1f", distance) + " blocks");

                // Inventar-Items auflisten
                List<Item> inventory = new ArrayList<>();
                for (int i = 0; i < finalClosestVillager.getInventory().getContainerSize(); i++) {
                    ItemStack stack = finalClosestVillager.getInventory().getItem(i);
                    if (!stack.isEmpty()) {
                        inventory.add(stack.getItem());
                    }
                }

                // Handelsangebote analysieren
                MerchantOffers offers = finalClosestVillager.getOffers();
                if (!offers.isEmpty()) {
                    for (MerchantOffer offer : offers) {
                        String inputA = offer.getBaseCostA().getCount() + "x " + offer.getBaseCostA().getHoverName().getString();
                        String inputB = offer.getCostB().isEmpty() ? "" : (" + " + offer.getCostB().getCount() + "x " + offer.getCostB().getHoverName().getString());
                        String result = offer.getResult().getCount() + "x " + offer.getResult().getHoverName().getString();
                        int priceDiff = offer.getSpecialPriceDiff();
                        String priceNote = (priceDiff != 0) ? " (price diff: " + priceDiff + ")" : "";
                        String tradeLine = inputA + inputB + " → " + result;
                        contextEntries.add("trade: " + tradeLine + priceNote);
                    }
                } else {
                    contextEntries.add("villager_trades: none");
                }

                // Weltinformationen ermitteln
                ServerLevel levelRef = (ServerLevel) finalClosestVillager.level();
                long dayTime = levelRef.getDayTime();
                long timeOfDay = dayTime % 24000;

                // Zeit in Worte und Uhrzeit umwandeln
                String timeOfDayLabel;
                int time = (int) timeOfDay;
                String time_formatted = convertTicksToTime(time);

                if (time <= 1000 && time >= 0) {
                    timeOfDayLabel = "Morgens";
                } else if (time <= 4666 && time > 1000) {
                    timeOfDayLabel = "Vormittag";
                } else if (time <= 7332 && time > 4666) {
                    timeOfDayLabel = "Mittag";
                } else if (time <= 12000 && time > 7332) {
                    timeOfDayLabel = "Nachmittag";
                } else if (time <= 13000 && time > 12000) {
                    timeOfDayLabel = "Abends";
                } else if (time <= 24000 && time > 13000) {
                    timeOfDayLabel = "Nacht";
                } else {
                    timeOfDayLabel = "Unknown";
                }

                boolean isDaytime = timeOfDay < 12000;

                // Weltkontextdaten hinzufügen
                contextEntries.add("world_time: " + dayTime);
                contextEntries.add("time_of_day: " + time_formatted + " (" + timeOfDayLabel + ")");
                contextEntries.add("day_count: Day " + (dayTime / 24000));
                contextEntries.add("is_daytime: " + isDaytime);
                contextEntries.add("is_raining: " + levelRef.isRaining());
                contextEntries.add("is_thundering: " + levelRef.isThundering());
                contextEntries.add("dimension: " + levelRef.dimension().location());

                // Biomname
                String biome = levelRef.getBiome(finalClosestVillager.blockPosition())
                        .unwrapKey()
                        .map(ResourceKey::location)
                        .map(Object::toString)
                        .orElse("unknown");
                contextEntries.add("biome: " + biome);

                // JSON-Array erzeugen
                StringBuilder contextJsonArray = new StringBuilder("[");
                for (int i = 0; i < contextEntries.size(); i++) {
                    contextJsonArray.append("\"").append(contextEntries.get(i).replace("\"", "\\\"")).append("\"");
                    if (i < contextEntries.size() - 1) {
                        contextJsonArray.append(", ");
                    }
                }
                contextJsonArray.append("]");

                // JSON-Payload für API
                String payload = String.format(
                        "{\"message\": \"%s\", \"context\": %s}",
                        message.replace("\"", "\\\""),
                        contextJsonArray.toString()
                );

                // HTTP POST an die externe Chat-API
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create("http://127.0.0.1:3000/chat"))
                        .header("Content-Type", "application/json")
                        .header("api-key", "<OPEN_AI_API_KEY>")
                        .POST(HttpRequest.BodyPublishers.ofString(payload))
                        .build();

                HttpClient client = HttpClient.newHttpClient();
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

                String json = response.body();
                String reply = parseReply(json);

                // Antwort im Spiel anzeigen (auf dem Server-Thread)
                context.getSource().getServer().execute(() -> {
                    context.getSource().sendSuccess(() -> Component.literal(finalClosestVillager.getName().getString() + ": " + reply), false);
                });

            } catch (Exception e) {
                // Fehlerbehandlung
                context.getSource().getServer().execute(() -> {
                    context.getSource().sendFailure(Component.literal("API call failed: " + e.getMessage()));
                });
            }
        });

        return 1;
    }

    // Extrahiert die "reply"-Antwort aus der JSON-Rückgabe der API
    private String parseReply(String json) {
        try {
            int start = json.indexOf("\"reply\":");
            if (start == -1) return json;
            int firstQuote = json.indexOf("\"", start + 8);
            int secondQuote = json.indexOf("\"", firstQuote + 1);
            if (firstQuote == -1 || secondQuote == -1) return json;
            return json.substring(firstQuote + 1, secondQuote);
        } catch (Exception e) {
            return json;
        }
    }

    // Konvertiert Minecraft-Ticks in reale Uhrzeit (Start bei 6 Uhr morgens)
    public static String convertTicksToTime(int ticks) {
        int totalMinutes = (ticks * 1440) / 24000;
        int hours = (totalMinutes / 60) + 6;
        int minutes = totalMinutes % 60;
        if (hours >= 24) {
            hours -= 24;
        }
        return String.format("%02d:%02d", hours, minutes);
    }

    // Clientseitige Events (z.B. Spielername im Log ausgeben)
    @Mod.EventBusSubscriber(modid = MODID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static class ClientModEvents {
        @SubscribeEvent
        public static void onClientSetup(FMLClientSetupEvent event) {
            LOGGER.info("CLIENT Setup complete");
            LOGGER.info("MINECRAFT NAME >> {}", Minecraft.getInstance().getUser().getName());
        }
    }
}