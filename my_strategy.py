import model
from model import AutoAttack, EntityType, EntityAction, AttackAction, BuildAction, Vec2Int, Player, MoveAction, \
    RepairAction


class MyStrategy:
    def __init__(self):
        self.actions = {}
        self.builders = []
        self.squad = []
        self.map = []
        self.drilling = False
        self.bar = False
        self.houses = [Vec2Int(0,0), Vec2Int(3,0), Vec2Int(0,3), Vec2Int(6,0), Vec2Int(0,6), Vec2Int(9,0), Vec2Int(0,9)]
        self.turrets = [Vec2Int(6,21), Vec2Int(21,6), Vec2Int(13,19), Vec2Int(19,13), Vec2Int(10,21), Vec2Int(21,10), Vec2Int(2,21), Vec2Int(21,2)]

    def get_action(self, player_view, debug_interface):
        print(player_view.entity_properties[2].max_health)
        self.map = [[0 for i in range(0, player_view.map_size)] for j in range(0, player_view.map_size)]
        for player in player_view.players:
            if player.id == player_view.my_id:
                me = player
        self.actions = {}
        entities_map = {}
        for i in range(0, 10):
            entities_map[i] = []
        for obj in player_view.entities:
            self.map[obj.position.x][obj.position.y]=1
            if obj.player_id == player_view.my_id:
                entities_map[obj.entity_type].append(obj)
        food = len(entities_map[3]) + len(entities_map[5] + entities_map[7])
        max_food = (len(entities_map[4]) + len(entities_map[2]) + len(entities_map[1]) + len(entities_map[6]))*5
        for i in range(0,10):
        
            if i==3: #Рабы
                for obj in entities_map[i]:
                    if obj not in self.builders:
                        entity_action = EntityAction(None, None, AttackAction(None, AutoAttack(200,[8])), None)
                        self.actions[obj.id] = entity_action
        
            '''if (food==max_food):
                self.build(1,Vec2Int(0+len(entities_map[1])*3,0),entities_map[3][0],player_view)'''
        
            if i==1: #Еда
                for obj in entities_map[i]:
                    if obj.health != player_view.entity_properties[1].max_health:
                        print('Обнаружено строение')
                        self.builders.append(entities_map[3][0])
                        self.repair(obj,obj.position,entities_map[3][0],player_view)
        
            if i ==2: #База
                for obj in entities_map[i]:
                    if len(entities_map[3])<15:
                        if len(entities_map[3])==14:
                            self.bar = True
                        vec = Vec2Int(obj.position.x, obj.position.y-1)
                        build = BuildAction(3,vec)
                        entity_action = EntityAction(None, build, None, None)
                        self.actions[obj.id] = entity_action
                    else:
                        vec = Vec2Int(obj.position.x, obj.position.y - 1)
                        build = BuildAction(3, vec)
                        entity_action = EntityAction(None, None, None, None)
                        self.actions[obj.id] = entity_action
        
            if self.bar:
                build(9, self.turrets[len(entities_map[9])], entities_map[3][0], player_view)
                
        
            if i==6: #Ренж казармы
                for obj in entities_map[i]:
                    if len(entities_map[3])==16 and len(entities_map[7])<3:
                        vec = Vec2Int(obj.position.x+len(entities_map[7]), obj.position.y-1)
                        build = BuildAction(7, vec)
                        entity_action = EntityAction(None, build, None, None)
                        self.actions[obj.id] = entity_action
                    else:
                        self.actions[obj.id] = EntityAction(None, None, None, None)
        
            if i == 7: #Ренжи
                if len(entities_map[7])==1:
                    vec = Vec2Int(25,2)
                    move = MoveAction(vec, True, False)
                    entity_action = EntityAction(move, None, None, None)
                    self.actions[entities_map[7][0].id] = entity_action
                else:
                    self.drill(sorted(entities_map[7], key=lambda range:range.id), Vec2Int(50, 50), self.map)
        return model.Action(self.actions)

    def build(self, type, position, builder, player_view):
        buildx = position.x+player_view.entity_properties[type].size-1
        buildy = position.y+player_view.entity_properties[type].size
        vec = Vec2Int(buildx, buildy)
        if not (builder.position.x == buildx and builder.position.y == buildy):
            move = MoveAction(vec,True,False)
            entity_action = EntityAction(move,None,None,None)
            self.actions[builder.id] = entity_action
        else:
            build = BuildAction(type, position)
            entity_action = EntityAction(None,build,None,None)
            self.actions[builder.id] = entity_action

    def destroy_find(self, map):
        pass

    def drill(self, drillers, drill_pos, map):
        if not self.drilling:
            for i in range(1, len(drillers)):
                print('Я выехал')
                if not (drillers[i].position.x == drillers[i-1].position.x - 1 and drillers[i].position.y == drillers[i-1].position.y):
                    vec = Vec2Int(drillers[i-1].position.x-1, drillers[i-1].position.y)
                    move = MoveAction(vec, True, False)
                    entity_action = EntityAction(move, None, None, None)
                    self.actions[drillers[i].id] = entity_action

    def repair(self,target,position,builder, player_view):
        type = target.entity_type
        buildx = position.x+player_view.entity_properties[type].size-1
        buildy = position.y+player_view.entity_properties[type].size
        vec = Vec2Int(buildx, buildy)
        if not (builder.position.x == buildx and builder.position.y == buildy):
            move = MoveAction(vec, None, None)
            entity_action = EntityAction(move, None, None, None)
            self.actions[builder.id] = entity_action
        else:
            entity_action = EntityAction(None, None, None, RepairAction(target.id))
            self.actions[builder.id] = entity_action

    def debug_update(self, player_view, debug_interface):
        debug_interface.send(model.DebugCommand.Clear())
        debug_interface.get_state()
