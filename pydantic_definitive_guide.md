# Documentação Definitiva do Pydantic

O Pydantic é a biblioteca de validação de dados mais utilizada para Python, conhecida por sua velocidade e extensibilidade. Ele permite definir como os dados devem ser em Python 3.9+ puro e canônico, e então validá-los de forma eficiente. Esta documentação visa ser um guia exaustivo sobre todos os seus principais conceitos, funcionalidades, decoradores, tipos e integrações, superando qualquer guia básico e fornecendo uma referência completa para desenvolvedores.

## Sumário

1.  [Introdução ao Pydantic](#1-introdução-ao-pydantic)
    *   [Por que usar Pydantic?](#por-que-usar-pydantic)
    *   [Instalação](#instalação)
2.  [Modelos (Models)](#2-modelos-models)
    *   [BaseModel](#basemodel)
    *   [Campos (Fields)](#campos-fields)
    *   [Tipos de Dados](#tipos-de-dados)
    *   [Validação de Dados](#validação-de-dados)
    *   [Configuração de Modelos](#configuração-de-modelos)
3.  [Validação de Dados](#3-validação-de-dados)
    *   [Validadores de Campo](#validadores-de-campo)
    *   [Validadores de Modelo](#validadores-de-modelo)
    *   [Modo Estrito (Strict Mode) vs. Modo Flexível (Lax Mode)](#modo-estrito-strict-mode-vs-modo-flexível-lax-mode)
4.  [Tipos de Dados Suportados](#4-tipos-de-dados-suportados)
    *   [Tipos Padrão do Python](#tipos-padrão-do-python)
    *   [Tipos Pydantic](#tipos-pydantic)
    *   [Tipos Genéricos](#tipos-genéricos)
    *   [Tipos Personalizados](#tipos-personalizados)
5.  [Decoradores e Funções](#5-decoradores-e-funções)
    *   [`@validator`](#validator)
    *   [`@root_validator`](#root_validator)
    *   [`@field_validator`](#field_validator)
    *   [`@model_validator`](#model_validator)
    *   [`Field()`](#field)
    *   [`ConfigDict`](#configdict)
6.  [Serialização e Desserialização](#6-serialização-e-desserialização)
    *   [`model_dump()`](#model_dump)
    *   [`model_dump_json()`](#model_dump_json)
    *   [`model_validate()`](#model_validate)
    *   [`model_validate_json()`](#model_validate_json)
7.  [Integrações e Ecossistema](#7-integrações-e-ecossistema)
    *   [FastAPI](#fastapi)
    *   [SQLModel](#sqlmodel)
    *   [Pydantic-Settings](#pydantic-settings)
    *   [JSON Schema](#json-schema)
8.  [Pydantic V2: Novidades e Migração](#8-pydantic-v2-novidades-e-migração)
    *   [Melhorias de Performance](#melhorias-de-performance)
    *   [Mudanças na API](#mudanças-na-api)
    *   [Modo Estrito](#modo-estrito)
9.  [Referências](#9-referências)

---

## 1. Introdução ao Pydantic

O Pydantic é uma biblioteca de validação de dados e análise de configurações que utiliza as anotações de tipo do Python para definir esquemas de dados. Ele garante que os dados de entrada correspondam a um formato e tipo esperados, levantando erros claros quando a validação falha. Além disso, o Pydantic oferece funcionalidades de serialização e desserialização, tornando-o uma ferramenta poderosa para trabalhar com APIs, bancos de dados e outras fontes de dados estruturados.

### Por que usar Pydantic?

*   **Tipagem Forte e Validação:** Utiliza as anotações de tipo do Python para definir a estrutura dos dados, validando-os automaticamente na criação da instância do modelo.
*   **Performance:** O core de validação do Pydantic V2 é escrito em Rust, o que o torna uma das bibliotecas de validação de dados mais rápidas para Python [1].
*   **Integração com IDEs e Linters:** Devido ao uso de type hints, o Pydantic se integra perfeitamente com ferramentas de análise estática e IDEs, oferecendo autocompletar e verificação de erros em tempo real.
*   **Geração de JSON Schema:** Modelos Pydantic podem gerar automaticamente JSON Schema, facilitando a documentação de APIs e a interoperabilidade com outras ferramentas [1].
*   **Flexibilidade:** Suporta modos de validação estrito e flexível, permitindo controlar o nível de coerção de dados [1].
*   **Ecossistema Robusto:** É a base de muitas bibliotecas populares, como FastAPI, SQLModel e Pydantic-Settings, e é amplamente utilizado na indústria [1].

### Instalação

A instalação do Pydantic é simples via `pip`:

```bash
pip install pydantic
```

Para a versão V2, que é a recomendada e a mais recente:

```bash
pip install -U pydantic
```

## 2. Modelos (Models)

O coração do Pydantic são os modelos, que são classes Python que herdam de `pydantic.BaseModel`. Eles definem a estrutura e os tipos esperados para seus dados.

### BaseModel

`BaseModel` é a classe base para todos os modelos Pydantic. Ao herdar dela, sua classe ganha capacidades de validação, serialização e outras funcionalidades do Pydantic.

```python
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

# Criação de uma instância com validação
data = {
    "id": 123,
    "signup_ts": "2023-01-01T10:00:00",
    "friends": [1, 2, 3]
}
user = User(**data)

print(user.id)          # Saída: 123
print(user.name)        # Saída: John Doe
print(user.signup_ts)   # Saída: 2023-01-01 10:00:00
print(user.friends)     # Saída: [1, 2, 3]

# Tentativa de criar com dados inválidos (levantará ValidationError)
try:
    User(id="abc")
except Exception as e:
    print(e)
```

### Campos (Fields)

Os atributos de um `BaseModel` são considerados campos. Eles podem ter tipos simples (int, str, bool), tipos complexos (list, dict, datetime), ou até mesmo outros modelos Pydantic.

#### Valores Padrão

Campos podem ter valores padrão, que serão usados se nenhum valor for fornecido durante a criação da instância.

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float = 0.0
    is_available: bool = True

product1 = Product(name="Laptop")
print(product1) # Saída: name='Laptop' price=0.0 is_available=True

product2 = Product(name="Mouse", price=25.50)
print(product2) # Saída: name='Mouse' price=25.5 is_available=True
```

#### Campos Opcionais

Use `Optional` (ou `| None` no Python 3.10+) para campos que podem ser `None`.

```python
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None # Ou description: str | None = None

item1 = Item(name="Caneta")
print(item1) # Saída: name='Caneta' description=None

item2 = Item(name="Livro", description="Um livro de ficção científica")
print(item2) # Saída: name='Livro' description='Um livro de ficção científica'
```

### Tipos de Dados

O Pydantic suporta uma vasta gama de tipos de dados, incluindo:

*   **Tipos Python nativos:** `str`, `int`, `float`, `bool`, `list`, `dict`, `tuple`, `set`, `bytes`.
*   **Tipos da biblioteca `typing`:** `Optional`, `Union`, `Literal`, `Any`, `List`, `Dict`, `Tuple`, `Set`, `FrozenSet`, `Deque`, `Pattern`, `Type`.
*   **Tipos de `datetime`:** `datetime`, `date`, `time`, `timedelta`.
*   **Tipos de `uuid`:** `UUID`.
*   **Tipos de `pathlib`:** `Path`.
*   **Tipos Pydantic específicos:** `EmailStr`, `HttpUrl`, `IPvAnyAddress`, `SecretStr`, `SecretBytes`, `FilePath`, `DirectoryPath`, `Json` e muitos outros.

### Validação de Dados

Quando uma instância de um `BaseModel` é criada, o Pydantic valida automaticamente os dados de entrada contra os tipos definidos. Se os dados não corresponderem, um `ValidationError` é levantado.

```python
from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    name: str
    age: int

try:
    Person(name="Alice", age="vinte") # 'vinte' não é um int
except ValidationError as e:
    print(e.errors())
    # Saída (simplificada):
    # [{'type': 'int_parsing', 'loc': ('age',), 'msg': 'Input should be a valid integer...'}]
```

### Configuração de Modelos

Modelos Pydantic podem ser configurados usando a classe `ConfigDict` (Pydantic V2) ou `Config` (Pydantic V1) aninhada. Isso permite controlar o comportamento do modelo, como alias de campo, extras permitidos, validação de atribuição, etc.

```python
from pydantic import BaseModel, ConfigDict

class MyModel(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    name: str
    value: int

try:
    # 'extra' está definido como 'forbid', então 'extra_field' causará um erro
    MyModel(name="Test", value=1, extra_field="oops")
except Exception as e:
    print(e)

# 'frozen' está definido como True, então a atribuição após a criação causará um erro
model_instance = MyModel(name="Immutable", value=10)
try:
    model_instance.value = 20
except Exception as e:
    print(e)
```

## 3. Validação de Dados

O Pydantic oferece mecanismos poderosos para validar dados, desde a validação automática de tipos até validadores personalizados complexos.

### Validadores de Campo

Validadores de campo são funções que são executadas em um campo específico após a validação de tipo básica. Eles são definidos usando o decorador `@field_validator` (Pydantic V2) ou `@validator` (Pydantic V1).

```python
from pydantic import BaseModel, field_validator

class UserProfile(BaseModel):
    username: str
    email: str

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @field_validator('email')
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Email must contain an @ symbol')
        return v

try:
    UserProfile(username="user_name", email="invalid-email.com")
except Exception as e:
    print(e)

user = UserProfile(username="validuser123", email="valid@example.com")
print(user)
```

### Validadores de Modelo

Validadores de modelo são funções que são executadas após a validação de todos os campos individuais. Eles são úteis para validações que dependem de múltiplos campos. Definidos com `@model_validator` (Pydantic V2) ou `@root_validator` (Pydantic V1).

```python
from pydantic import BaseModel, model_validator

class Event(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def check_dates_order(self) -> 'Event':
        if self.start_date >= self.end_date:
            raise ValueError('End date must be after start date')
        return self

try:
    Event(start_date="2023-01-01T10:00:00", end_date="2023-01-01T09:00:00")
except Exception as e:
    print(e)

event = Event(start_date="2023-01-01T10:00:00", end_date="2023-01-01T11:00:00")
print(event)
```

### Modo Estrito (Strict Mode) vs. Modo Flexível (Lax Mode)

O Pydantic V2 introduziu o conceito de modos de validação:

*   **Modo Flexível (Lax Mode - padrão):** O Pydantic tenta coercer os dados para o tipo correto sempre que possível (ex: "123" para `int`, `[1, "2"]` para `list[int]`).
*   **Modo Estrito (Strict Mode):** O Pydantic não tenta coercer os dados. Os dados de entrada devem corresponder exatamente ao tipo anotado. Isso é útil para garantir a integridade dos dados e evitar conversões inesperadas.

Você pode definir o modo globalmente ou por modelo:

```python
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)

    value: int

try:
    StrictModel(value="123") # Erro no modo estrito
except Exception as e:
    print(e)

class LaxModel(BaseModel):
    value: int

lax_instance = LaxModel(value="123") # Funciona no modo flexível
print(lax_instance.value)
```

## 4. Tipos de Dados Suportados

O Pydantic se integra profundamente com o sistema de tipos do Python, suportando uma vasta gama de tipos.

### Tipos Padrão do Python

*   `str`, `int`, `float`, `bool`, `bytes`
*   `list`, `tuple`, `set`, `dict`, `frozenset`
*   `datetime.datetime`, `datetime.date`, `datetime.time`, `datetime.timedelta`
*   `uuid.UUID`
*   `pathlib.Path`
*   `enum.Enum`

### Tipos Pydantic

O Pydantic fornece tipos adicionais para validações mais específicas:

*   `EmailStr`: Valida se a string é um endereço de e-mail válido.
*   `HttpUrl`: Valida se a string é uma URL HTTP(S) válida.
*   `IPvAnyAddress`, `IPvAnyInterface`, `IPvAnyNetwork`: Para endereços IP.
*   `FilePath`, `DirectoryPath`: Para caminhos de arquivo/diretório que existem.
*   `SecretStr`, `SecretBytes`: Para dados sensíveis que não devem ser expostos em logs ou representações de string.
*   `Json`: Para campos que devem conter JSON válido.
*   `PositiveInt`, `NegativeInt`, `NonNegativeInt`, `NonPositiveInt`: Para validação de números inteiros com restrições de sinal.
*   `PositiveFloat`, `NegativeFloat`, `NonNegativeFloat`, `NonPositiveFloat`: Para validação de números de ponto flutuante com restrições de sinal.

**Exemplo:**

```python
from pydantic import BaseModel, EmailStr, HttpUrl, Field

class UserContact(BaseModel):
    email: EmailStr
    website: HttpUrl
    age: int = Field(gt=0, lt=150) # Idade maior que 0 e menor que 150

try:
    UserContact(email="invalid-email", website="not-a-url", age=-5)
except Exception as e:
    print(e)

contact = UserContact(email="test@example.com", website="https://www.pydantic.dev", age=30)
print(contact)
```

### Tipos Genéricos

O Pydantic suporta modelos genéricos, permitindo criar estruturas de dados reutilizáveis que podem ser parametrizadas com diferentes tipos.

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    status: str
    data: T

class UserData(BaseModel):
    id: int
    name: str

# Resposta com dados de usuário
user_response = Response[UserData](status="success", data=UserData(id=1, name="Alice"))
print(user_response.data.name)

# Resposta com uma lista de strings
list_response = Response[list[str]](status="success", data=["item1", "item2"])
print(list_response.data[0])
```

### Tipos Personalizados

Você pode definir seus próprios tipos personalizados e integrá-los ao Pydantic usando `Annotated` ou criando classes que herdam de tipos Pydantic existentes.

## 5. Decoradores e Funções

### `@validator` (Pydantic V1) / `@field_validator` (Pydantic V2)

Usado para adicionar validação personalizada a um ou mais campos. No Pydantic V2, `@field_validator` é o sucessor, com um uso ligeiramente diferente (requer `mode='before'` ou `mode='after'` e `classmethod`).

**Exemplo (Pydantic V2):**

```python
from pydantic import BaseModel, field_validator

class MyModel(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def check_value_length(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError('Value must be at least 5 characters long')
        return v

try:
    MyModel(value="short")
except Exception as e:
    print(e)
```

### `@root_validator` (Pydantic V1) / `@model_validator` (Pydantic V2)

Usado para validação que depende de múltiplos campos do modelo. No Pydantic V2, `@model_validator` é o sucessor, com `mode='before'` (para dados brutos) ou `mode='after'` (para a instância do modelo).

**Exemplo (Pydantic V2):**

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start: datetime
    end: datetime

    @model_validator(mode='after')
    def check_dates(self) -> 'DateRange':
        if self.start >= self.end:
            raise ValueError('End date must be after start date')
        return self

try:
    DateRange(start="2023-01-01", end="2022-12-31")
except Exception as e:
    print(e)
```

### `Field()`

Usado para fornecer metadados adicionais para campos do modelo, como valores padrão, alias, descrições, exemplos e restrições de validação (ex: `min_length`, `max_length`, `gt`, `lt`).

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., description="ID único do usuário", gt=0)
    name: str = Field("Anônimo", min_length=2, max_length=50)
    email: EmailStr = Field(..., alias="user_email")

user = User(id=1, user_email="test@example.com")
print(user.model_dump(by_alias=True)) # Saída: {'id': 1, 'name': 'Anônimo', 'user_email': 'test@example.com'}
```

### `ConfigDict` (Pydantic V2)

Substitui a classe `Config` do Pydantic V1 para configurar o comportamento do modelo. É importado diretamente de `pydantic`.

**Parâmetros comuns:**

*   `extra`: Controla o que acontece com campos extras não definidos no modelo (`'ignore'`, `'allow'`, `'forbid'`).
*   `populate_by_name`: Se `True`, permite que os campos sejam populados usando seus aliases.
*   `json_schema_extra`: Um dicionário ou função para adicionar metadados extras ao JSON Schema gerado.
*   `strict`: Se `True`, ativa o modo estrito para o modelo.
*   `frozen`: Se `True`, torna as instâncias do modelo imutáveis.

**Exemplo:**

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

    name: str
    age: int

try:
    StrictUser(name="Bob", age="25", city="New York") # 'city' é extra e 'age' é string
except Exception as e:
    print(e)
```

## 6. Serialização e Desserialização

O Pydantic facilita a conversão de modelos Python para formatos como JSON e vice-versa.

### `model_dump()`

Converte a instância do modelo em um dicionário Python. Útil para inspeção ou para passar dados para outras bibliotecas.

**Parâmetros comuns:**

*   `mode`: `'json'` (padrão) ou `'python'`. Controla como os tipos são serializados.
*   `include`, `exclude`: Campos a incluir/excluir.
*   `by_alias`: Se `True`, usa os aliases dos campos como chaves do dicionário.
*   `exclude_unset`: Se `True`, exclui campos que não foram definidos explicitamente.

**Exemplo:**

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "John Doe"
    email: EmailStr

user_instance = User(id=1, email="test@example.com")
user_dict = user_instance.model_dump()
print(user_dict) # Saída: {'id': 1, 'name': 'John Doe', 'email': 'test@example.com'}

user_dict_alias = user_instance.model_dump(by_alias=True)
print(user_dict_alias)
```

### `model_dump_json()`

Converte a instância do modelo em uma string JSON.

**Parâmetros:**

Os parâmetros são os mesmos de `model_dump()`.

**Exemplo:**

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

user_instance = User(id=1, name="Alice", email="alice@example.com")
user_json = user_instance.model_dump_json()
print(user_json) # Saída: {
"id":1,"name":"Alice","email":"alice@example.com"}
```

### `model_validate(obj: Any, *, strict: bool | None = None, from_attributes: bool | None = None)`

Valida um objeto arbitrário e retorna uma instância do modelo. É o método preferido para criar modelos a partir de dados brutos.

**Parâmetros:**

*   `obj` (`Any`): O objeto a ser validado (geralmente um dicionário).
*   `strict` (`bool | None`): Sobrescreve a configuração `strict` do modelo para esta validação.
*   `from_attributes` (`bool | None`): Se `True`, tenta ler atributos do objeto (útil para ORMs). O padrão é `None` (comportamento padrão do modelo).

**Exemplo:**

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float

data = {"name": "Teclado", "price": 79.99}
product = Product.model_validate(data)
print(product)

# Exemplo com dados inválidos
try:
    Product.model_validate({"name": "Mouse", "price": "abc"})
except Exception as e:
    print(e)
```

### `model_validate_json(json_data: str | bytes, *, strict: bool | None = None)`

Valida uma string JSON e retorna uma instância do modelo.

**Parâmetros:**

*   `json_data` (`str | bytes`): A string JSON a ser validada.
*   `strict` (`bool | None`): Sobrescreve a configuração `strict` do modelo para esta validação.

**Exemplo:**

```python
from pydantic import BaseModel

class Order(BaseModel):
    item_id: int
    quantity: int

json_str = '{"item_id": 101, "quantity": 2}'
order = Order.model_validate_json(json_str)
print(order)

# Exemplo com JSON inválido
try:
    Order.model_validate_json('{"item_id": "abc", "quantity": 1}')
except Exception as e:
    print(e)
```

## 7. Integrações e Ecossistema

O Pydantic é a base de um vasto ecossistema de bibliotecas e ferramentas Python, impulsionando o desenvolvimento de aplicações robustas e tipadas.

### FastAPI

O [FastAPI](https://fastapi.tiangolo.com/) utiliza o Pydantic para definir esquemas de requisição e resposta, validação automática de dados, serialização e geração de documentação interativa (OpenAPI/Swagger UI).

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### SQLModel

[SQLModel](https://sqlmodel.tiangolo.com/) é uma biblioteca que combina o poder do Pydantic e do SQLAlchemy para criar modelos de dados que funcionam tanto como modelos Pydantic (para validação e serialização) quanto como modelos SQLAlchemy (para interação com bancos de dados).

```python
from typing import Optional
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

# Hero pode ser usado como um modelo Pydantic para validação
hero_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
hero = Hero(**hero_data)
print(hero)
```

### Pydantic-Settings

A biblioteca [Pydantic-Settings](https://pydantic-docs.helpmanual.io/pydantic-settings/) (anteriormente parte do Pydantic, agora um pacote separado) permite gerenciar configurações de aplicativos de forma tipada, carregando-as de variáveis de ambiente, arquivos `.env` e outros formatos.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "MyApp"
    database_url: str
    debug: bool = False

# Supondo um arquivo .env com DATABASE_URL=sqlite:///./test.db
settings = Settings()
print(settings.app_name)
print(settings.database_url)
print(settings.debug)
```

### JSON Schema

Uma das grandes vantagens do Pydantic é a capacidade de gerar [JSON Schema](https://json-schema.org/) a partir de seus modelos. Isso é inestimável para documentação de API, validação de dados em diferentes linguagens e interoperabilidade.

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    tags: list[str] = []

print(Product.model_json_schema())
# Saída (exemplo parcial):
# {
#     'properties': {
#         'name': {'title': 'Name', 'type': 'string'},
#         'price': {'title': 'Price', 'type': 'number'},
#         'tags': {'default': [], 'title': 'Tags', 'type': 'array', 'items': {'type': 'string'}}
#     },
#     'required': ['name', 'price'],
#     'title': 'Product', 'type': 'object'
# }
```

## 8. Pydantic V2: Novidades e Migração

O Pydantic V2 representa uma reescrita completa da biblioteca, trazendo melhorias significativas de performance e novas funcionalidades, além de algumas mudanças na API. É a versão recomendada para novos projetos.

### Melhorias de Performance

O Pydantic V2 foi reescrito em Rust, o que resultou em ganhos de performance de 5x a 50x em comparação com o Pydantic V1, dependendo do caso de uso [1]. Isso o torna ideal para aplicações de alta performance.

### Mudanças na API

Algumas das mudanças mais notáveis na API incluem:

*   **`Config` para `ConfigDict`:** A classe `Config` aninhada foi substituída por `model_config = ConfigDict(...)`.
*   **`@validator` para `@field_validator` e `@model_validator`:** Os decoradores de validação foram separados para maior clareza e controle.
*   **Métodos de Modelo:** Métodos como `dict()`, `json()`, `parse_obj()`, `parse_raw()` foram renomeados para `model_dump()`, `model_dump_json()`, `model_validate()`, `model_validate_json()` respectivamente, para evitar conflitos com nomes de campos.
*   **Modo Estrito:** Introdução do `strict=True` para validação sem coerção de tipos.
*   **`Field`:** Novas opções e melhorias para a função `Field()`.

Para uma lista completa das mudanças e um guia de migração detalhado, consulte a [documentação oficial de migração do Pydantic V2](https://docs.pydantic.dev/latest/migration/).

### Modo Estrito

O modo estrito é uma das adições mais importantes do Pydantic V2. Ele força a validação de tipo exata, sem tentar coercer valores. Isso pode ser ativado globalmente ou por modelo usando `ConfigDict(strict=True)`.

```python
from pydantic import BaseModel, ConfigDict, ValidationError

class StrictData(BaseModel):
    model_config = ConfigDict(strict=True)

    value: int

try:
    StrictData(value="123") # Falha no modo estrito
except ValidationError as e:
    print(e.errors())

strict_instance = StrictData(value=123) # Sucesso
print(strict_instance)
```

## 9. Referências

[1] [Welcome to Pydantic - Pydantic Validation](https://docs.pydantic.dev/latest/)
[2] [Models - Pydantic Validation](https://docs.pydantic.dev/latest/concepts/models/)
[3] [Fields - Pydantic Validation](https://docs.pydantic.dev/latest/concepts/fields/)
[4] [Types - Pydantic Validation](https://docs.pydantic.dev/latest/concepts/types/)
[5] [Pydantic V2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
[6] [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
[7] [SQLModel Official Documentation](https://sqlmodel.tiangolo.com/)
[8] [Pydantic-Settings Documentation](https://pydantic-docs.helpmanual.io/pydantic-settings/)
[9] [JSON Schema Official Website](https://json-schema.org/)
[10] [12-factor app](https://12factor.net/)
