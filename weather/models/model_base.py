from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from weather.models import DBDriver
from sqlalchemy.exc import (AmbiguousForeignKeysError, ArgumentError,
                            CircularDependencyError, CompileError,
                            DatabaseError, DataError, DBAPIError,
                            DisconnectionError, IdentifierError,
                            IntegrityError, InterfaceError, InternalError,
                            InvalidatePoolError, InvalidRequestError,
                            NoForeignKeysError, NoInspectionAvailable,
                            NoReferencedColumnError, NoReferencedTableError,
                            NoReferenceError, NoSuchColumnError,
                            NoSuchModuleError, NoSuchTableError,
                            NotSupportedError, ObjectNotExecutableError,
                            OperationalError, ProgrammingError,
                            ResourceClosedError, SQLAlchemyError,
                            StatementError)
from sqlalchemy.exc import TimeoutError as TimeoutErrorSql
from sqlalchemy.exc import (UnboundExecutionError, UnreflectableTableError,
                            UnsupportedCompilationError)

Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True

    KNOWN_ERROR_SQLALCHEMY = {'friendly_message': 'Database error contact system admin, this action was logged.',
                              'known_errors': (
                                  IntegrityError, AmbiguousForeignKeysError,
                                  CircularDependencyError,
                                  ArgumentError,
                                  CompileError,
                                  DatabaseError,
                                  DataError,
                                  DBAPIError,
                                  DisconnectionError,
                                  IdentifierError,
                                  IntegrityError,
                                  InterfaceError,
                                  InternalError,
                                  InvalidatePoolError,
                                  InvalidRequestError,
                                  NoForeignKeysError,
                                  NoInspectionAvailable,
                                  NoReferencedColumnError,
                                  NoReferencedTableError,
                                  NoReferenceError,
                                  NoSuchColumnError,
                                  NoSuchModuleError,
                                  NoSuchTableError,
                                  NotSupportedError,
                                  ObjectNotExecutableError,
                                  OperationalError,
                                  ProgrammingError,
                                  ResourceClosedError,
                                  SQLAlchemyError,
                                  StatementError,
                                  TimeoutErrorSql,
                                  UnboundExecutionError,
                                  UnreflectableTableError,
                                  UnsupportedCompilationError,
                              )}

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def orm(self):
        return DBDriver()
