---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

+++ {"slideshow": {"slide_type": "slide"}}

# Le problème du fast-food

On se propose d'illustrer ici la puissance de la programmation asynchrone sur un cas très concret : celui du service dans un restaurant. L'objectif du TP est de vous faire sentir que l'on pense très aisément en asynchrone et que cela peut amener un gain de performances substantiel sur de petits programmes. 

Commençons d'abord comme d'habitude avec les imports :

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
import asyncio
import time
from datetime import datetime
from typing import List
from asynchelpers import start_timer, show_timer
```

L'idée du TP est de gérer des commandes variés. Chacune des commandes correspond à une liste d'articles qui mettent plus ou moins de temps à être préparés. Vous avez dans la cellule suivante deux dictionnaires : 
 * le premier `TASK_LENGTHS` qui associe à un article la durée de préparation nécessaire ; 
 * le deuxième `ORDERS` qui associe à des clients une liste d'articles. 
Vous pouvez bien entendu ajouter des éléments dans ces deux dictionnaires !

```{code-cell} ipython3
TASKS_LENGTHS = {
    'burger': 2.,
    'fries': 1.5,
    'soda': 0.5,
    'sundae': 1.,
    'coffee': 0.5
}

ORDERS = {
    'A': ['burger', 'fries', 'soda', 'sundae'],
    'B': ['burger', 'fries', 'soda'],
    'C': ['burger', 'burger', 'fries', 'sundae', 'soda'],
    'D': ['coffee'],
    'E': ['burger', 'fries'],
}
```

## Une première approche en programmation synchrone

Nous allons dans un premier temps tenter de résoudre le problème de manière synchrone. Pour cela écrire une fonction `execute(client: str, tasks: List[str])` qui prend en argument le nom du client et sa commande sous la forme d'une liste de chaînes de caractères. Le fragment de code :
```python
start_timer()
execute('A', ORDERS['A'])
```
doit produire une sortie du type: 
```
---------- zero
2s + 002ms burger for client A.
3s + 504ms fries for client A.
4s + 006ms soda for client A.
5s + 007ms sundae for client A.
```

```{code-cell} ipython3
def execute(client: str, tasks: List[str]):
    for name in tasks:
        time.sleep(TASKS_LENGTHS[name])
        show_timer(f"{name} for client {client}.")
```

```{code-cell} ipython3
# Vérifiez votre code ici
start_timer()
execute('A', ORDERS['A'])
```

Pour évaluer la performance du système, il nous faut calculer le temps écoulé entre la commande du client de le service. Pour cela, il faut encapsuler l'appel à `execute` dans un fonction `take_order(client: str, tasks: List[str], order_time: datetime)`. 

**Note :** on utilise ici `datetime.now()` pour récuperer le temps courant.

```{code-cell} ipython3
def take_order(client, tasks, order_time):
    show_timer(f"Client {client}'s order is treated.")
    execute(client, tasks)
    dtime = datetime.now() - order_time
    print(f">>> Client {client} served in {dtime.seconds} s + {dtime.microseconds//1000:03d} ms.")
```

```{code-cell} ipython3
# Voici un exemple d'appel
start_timer()
take_order('A', ORDERS['A'], datetime.now())
```

Intéressons nous maintenant au cas où plusieurs clients passent des commandes. On pourrait écrire le code suivant :

```{code-cell} ipython3
start_timer()
for client, tasks in ORDERS.items():
    take_order(client, tasks, datetime.now())
```

Ce code ne représente pas du tout la réalité, car on attend que la commande de `A` soit servie pour prendre celle de `B`. Bien que cela ressemble pas mal au fonctionnement actuel des restaurant, ce n'est pas *nominal*. 

Il faudrait donc être capables d'avoir un conteneur dans lequel on stocke les commandes quand elles sont passées et duquel la cuisine tire ses prochaines tâches. Dans le cadre de la programmation synchrone, cela peut se faire en créant deux objets `Process`. Le conteneur faisant le lien entre les deux sera une `Queue`. Un processus sera responsable d'ajouter les commandes dans la queue au fil de l'eau tandis que le deuxième traitera les commandes. 

**Note sur le fonctionnement des objets `Queue` :** ces objets présentent deux méthode principales :
 * la méthode `get` qui permet de récupérer l'élément le plus ancien de la queue. Si la queue est vide, l'appel est bloquant et on attend qu'un élément soit ajouté à la queue.
 * la méthode `put` qui permet d'ajouter un élément à la queue. 
Pour éviter d'avoir des `Process` qui ne se terminent jamais, il faut pouvoir indiquer à la `Queue` qu'elle a fini de travailler, c'est généralement fait en y mettant `None`. Le process écoutant la queue détecte cela et s'arrête.

**Note sur le fonctionnement des `Process` :** dans le TP actuel, nous allons avoir un usage assez simple des `Process`. Il seront créés et utilisés comme suit : 
```python
# Création des process
proc1 = Process(target=function_to_execute, args=function_args_as_tuple)
proc2 = Process(target=function2_to_execute, args=function2_args_as_tuple)

[p.start() for p in [proc1, proc2]]
[p.join() for p in [proc1, proc2]]
```

```{code-cell} ipython3
from multiprocessing import Queue, Process

def treat_orders(queue):
    while True:
        in_queue = queue.get()
        if in_queue is None:
              break
        take_order(*in_queue)
        
def make_orders(orders_dict, queue, delay):
    for client, tasks in orders_dict.items():
        order_time = datetime.now()
        print(f">>> Client {client} orders.")
        queue.put((client, tasks, order_time))
        time.sleep(delay)
    queue.put(None)
```

```{code-cell} ipython3
queue = Queue()

processes = [
    Process(target=make_orders, args=(ORDERS, queue, 1.2)),
    Process(target=treat_orders, args=(queue,))
]

start_timer()
[p.start() for p in processes]
[p.join() for p in processes]
show_timer("Finished")
```

```{code-cell} ipython3
async def async_execute(client, tasks):
    async def waiter(name):
        await asyncio.sleep(TASKS_LENGTHS[name])
        show_timer(f"{name} for client {client}.")

    await asyncio.ensure_future(asyncio.gather(*tuple(waiter(name) for name in tasks)))

async def async_take_order(client, tasks, order_time = None):
    if order_time is None:
        order_time = datetime.now()
    show_timer(f"Client {client}'s order is treated.")
    await async_execute(client, tasks)
    dtime = datetime.now() - order_time
    print(f">>> Client {client} served in {dtime.seconds} s + {dtime.microseconds//1000:03d} ms.")
```

```{code-cell} ipython3
start_timer()
await async_take_order('A', ORDERS['A'])
```

```{code-cell} ipython3
async def async_make_orders(orders_dict, delay):
    orders = []
    for client, tasks in orders_dict.items():
        order_time = datetime.now()
        print(f">>> Client {client} orders.")
        tsk = asyncio.ensure_future(async_take_order(client, tasks, order_time))
        orders.append(tsk)
        await asyncio.sleep(delay)
        
    await asyncio.wait(orders)
    show_timer("Finished")
```

```{code-cell} ipython3
start_timer()
await async_make_orders(ORDERS, 0.)
```

```{code-cell} ipython3
RESSOURCES= {
    'burger': asyncio.Semaphore(3),
    'fries': asyncio.Lock(),
    'sundae': asyncio.Lock(),
    'coffee': asyncio.Lock(),
    'soda': asyncio.Semaphore(2)
}

async def async_execute_ressources(client, tasks):
    async def waiter(name):
        async with RESSOURCES[name]:
            await asyncio.sleep(TASKS_LENGTHS[name])
            show_timer(f"{name} for client {client}.")

    await asyncio.ensure_future(asyncio.gather(*tuple(waiter(name) for name in tasks)))

async def async_take_order_ressources(client, tasks, order_time = None):
    if order_time is None:
        order_time = datetime.now()
    show_timer(f"Client {client}'s order is treated.")
    await async_execute_ressources(client, tasks)
    dtime = datetime.now() - order_time
    print(f">>> Client {client} served in {dtime.seconds} s + {dtime.microseconds//1000:03d} ms.")

async def async_make_orders_ressources(orders_dict, delay):
    orders = []
    for client, tasks in orders_dict.items():
        order_time = datetime.now()
        print(f">>> Client {client} orders.")
        local_order = asyncio.ensure_future(async_take_order_ressources(client, tasks, order_time))
        orders.append(local_order)
        await asyncio.sleep(delay)
        
    await asyncio.wait(orders)
    show_timer("Finished")
```

```{code-cell} ipython3
start_timer()
await async_make_orders_ressources(ORDERS, 0.)
```

L'idée originale de l'exercice vient de [ce post sur la programmation asynchrone en Python.](https://zestedesavoir.com/articles/1568/decouvrons-la-programmation-asynchrone-en-python/)