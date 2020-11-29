import model
from model import AutoAttack, EntityType, EntityAction, AttackAction, BuildAction, Vec2Int, Player, MoveAction


class MyStrategy:
    def __init__(self):
        self.actions = {}

    def get_action(self, player_view, debug_interface):
        for player in player_view.players:
            if player.id == player_view.my_id:
                me = player
        self.actions = {}
        entities_map = {}
        for i in range(0, 10):
            entities_map[i] = []
        for obj in player_view.entities:
            if obj.player_id == player_view.my_id:
                entities_map[obj.entity_type].append(obj)
        food = len(entities_map[3]) + len(entities_map[5] + entities_map[7])
        max_food = 15 + len(entities_map[1]) * 5
        for i in range(0,10):
            print(entities_map[1])
            if i==3:
                for obj in entities_map[i]:
                    entity_action = EntityAction(None, None, AttackAction(None, AutoAttack(200,[8])), None)
                    self.actions[obj.id] = entity_action
            if (food==max_food):
                self.build(1,Vec2Int(0+len(entities_map[1])*3,0),entities_map[3][0],player_view)
            if i ==2:
                for obj in entities_map[i]:
                    if len(entities_map[3])<200:
                        vec = Vec2Int(obj.position.x, obj.position.y-1)
                        build = BuildAction(3,vec)
                        entity_action = EntityAction(None, build, None, None)
                        self.actions[obj.id] = entity_action
                    else:
                        vec = Vec2Int(obj.position.x, obj.position.y - 1)
                        build = BuildAction(3, vec)
                        entity_action = EntityAction(None, None, None, None)
                        self.actions[obj.id] = entity_action
        return model.Action(self.actions)

    def build(self, type, position, builder, player_view):
        buildx = position.x+player_view.entity_properties[type].size-1
        buildy = position.y+player_view.entity_properties[type].size
        vec = Vec2Int(buildx, buildy)
        if not (builder.position.x == buildx and builder.position.y == buildy):
            move = MoveAction(vec,True,True)
            entity_action = EntityAction(move,None,None,None)
            self.actions[builder.id] = entity_action
        else:
            build = BuildAction(type, position)
            entity_action = EntityAction(None,build,None,None)
            self.actions[builder.id] = entity_action
    def debug_update(self, player_view, debug_interface):
        debug_interface.send(model.DebugCommand.Clear())
        debug_interface.get_state()
