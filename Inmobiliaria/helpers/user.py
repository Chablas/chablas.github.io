import json

def load_usuario(request):
    if(request.session.get('usuario') is None):
        return {}
    
    usuario = json.loads(request.session.get('usuario'))
    
    apellido_nombres = f"{usuario['apellidoPaterno']} {usuario['apellidoMaterno']}, {usuario['nombres']}"
    modulos = usuario['rol']['modulos']

    return {
        'apellidos_nombres': apellido_nombres,
        'mis_modulos': modulos
    }

def get_all_modulos():
    return [
        (1, 'Empleados'),
        (2, 'Proyectos'),
        (3, 'Etapas'),
        (4, 'Estados'),
        (5, 'Zonas'),
        (6, 'Categorias'),
        (7, 'Proveedores'),
        (8, 'Unidades de Medida'),
        (9, 'Roles'),
        (10, 'Tipos de archivo'),
        (11, 'Archivos'),
        (12, 'Tipos de documento'),
        (13, 'Actividades'),
        (14, 'Materiales'),
        (15, 'Independientes')
    ]

def menu(request):
    sidebar = [
        {
            'route' : 'administracion:index',
            'icon': 'fa-chart-pie',
            'title': 'Dashboard',
            'modulo': 0,
            'childs': None
        },
        {
            'route' : 'usuarios:empleadosIndex',
            'icon': 'fa-users',
            'title': 'Empleados',
            'modulo': 1,
            'childs': None
        },
        {
            'route' : 'usuarios:independientesIndex',
            'icon': 'fa-users',
            'title': 'Independientes',
            'modulo': 15,
            'childs': None
        },
        {
            'route' : 'gestion-proyectos',
            'icon': 'fa-city',
            'title': 'Proyectos',
            'modulos': [2,3,4,5],
            'childs': [
                {
                    'route' : 'proyectos:proyectosIndex',
                    'icon': 'fa-building',
                    'modulo': 2,
                    'title': 'Proyectos'
                },
                {
                    'route' : 'proyectos:etapasIndex',
                    'icon': 'fa-building-flag',
                    'modulo': 3,
                    'title': 'Etapas'
                },
                {
                    'route' : 'proyectos:estadosIndex',
                    'icon': 'fa-building-flag',
                    'modulo': 4,
                    'title': 'Estados'
                },
                {
                    'route' : 'proyectos:zonasIndex',
                    'icon': 'fa-building-flag',
                    'modulo': 5,
                    'title': 'Zonas'
                }
            ]
        },
        {
            'route' : 'gestion-almacen',
            'icon': 'fa-solid fa-warehouse',
            'title': 'Almacen',
            'modulos': [0],
            'childs': [
                {
                    'route' : 'almacen:materialIndex',
                    'icon': 'fa-solid fa-helmet-safety',
                    'modulo': 0,
                    'title': 'Materiales'
                }
            ]
        },
        {
            'route' : 'gestion-ordenes-compras',
            'icon': 'fa-clipboard-list',
            'title': 'Compras',
            'modulos': [0],
            'childs': [
                {
                    'route' : 'compras:pedidosIndex', 
                    'icon': 'fa-file',
                    'modulo': 0,
                    'title': 'Pedidos'
                },
                {
                    'route' : 'compras:comprasList', 
                    'icon': 'fa-file',
                    'modulo': 0,
                    'title': 'Ord. Compra'
                },
                {
                    'route' : 'compras:guiasRemisionIndex', 
                    'icon': 'fa-file',
                    'modulo': 0,
                    'title': 'Guias Remision'
                },
            ]
        },
        {
            'route' : 'gestion-proveedores',
            'icon': 'fa-user-tie',
            'title': 'Proveedores',
            'modulos': [6,7],
            'childs': [
                {
                    'route' : 'proveedores:categoriasIndex',
                    'icon': 'fa-tag',
                    'modulo': 6,
                    'title': 'Categorias'
                },
                {
                    'route' : 'proveedores:proveedoresIndex',
                    'icon': 'fa-user-tie',
                    'modulo': 7,
                    'title': 'Proveedores'
                }
            ]
        },
        {
            'route' : 'sistema',
            'icon': 'fa-shield',
            'title': 'Sistema',
            'modulos': [10, 12, 8, 13],
            'childs': [
                {
                    'route' : 'sistema:tiposArchivoIndex',
                    'modulo': 10,
                    'icon': 'fa-tag',
                    'title': 'Tipos de archivo'
                },
                {
                    'route' : 'sistema:tiposDocumentoIndex',
                    'modulo': 12,
                    'icon': 'fa-tag',
                    'title': 'Tipos documento'
                },
                {
                    'route' : 'sistema:actividadesIndex',
                    'icon': 'fa-tag',
                    'modulo': 13,
                    'title': 'Act. Materiales'
                },
                {   'route' : 'sistema:unidadesMedidaIndex',
                    'icon': 'fa-tag',
                    'modulo': 8,
                    'title': 'Unidades Medida'
                },
                {
                    'route' : 'sistema:empresaForm',
                    'modulo': 0,
                    'icon': 'fa-tag',
                    'title': 'Empresa'
                }
            ]
        },
        {
            'route' : 'seguridad',
            'icon': 'fa-shield',
            'title': 'Seguridad',
            'modulos': [9],
            'childs': [
                {
                    'route' : 'seguridad:rolesIndex',
                    'modulo': 9,
                    'icon': 'fa-tag',
                    'title': 'Roles'
                },
                {
                    'route' : 'seguridad:logsIndex',
                    'modulo': 0,
                    'icon': 'fa-tag',
                    'title': 'Logs'
                }
            ]
        },
    ]
    
    return {'sidebar': sidebar}
