#ifndef STRLEN
#  define STRLEN 81
#endif
#define _true 1
#define _false 0
typedef unsigned char boolean;
typedef int integer;
typedef char* string;
void DRIVE_I_a(void);
void DRIVE_I_b(void);
int DRIVE(void);
int DRIVE_reset(void);
#ifndef _NO_EXTERN_DEFINITIONS
#  ifndef _NO_CONSTANT_DEFINITIONS
#  endif /* _NO_CONSTANT_DEFINITIONS */
#  ifndef _NO_FUNCTION_DEFINITIONS
#  endif /* _NO_FUNCTION_DEFINITIONS */
#  ifndef _NO_PROCEDURE_DEFINITIONS
#  endif /* _NO_PROCEDURE_DEFINITIONS */
#endif /* _NO_EXTERN_DEFINITIONS */

static struct {
  unsigned int a : 1;
  unsigned int b : 1;
  unsigned int o : 1;
} _s = {  0,  0,  0 };
#define tick 1
static unsigned char _state_1 = 1;
static unsigned char _state_3;
static unsigned char _state_7;
static int _term_21;
void DRIVE_I_a(void) {
  _s.a = 1;
}
void DRIVE_I_b(void) {
  _s.b = 1;
}

int DRIVE(void)
{
	_term_21=-1;
  /* Vacuous terminate */;
  if (_state_1) {
    _s.o = 0;;
    _state_1 = 0;
    _state_7 = 1;
    /* Vacuous terminate */;
    _state_3 = 1;
    /* Vacuous terminate */;
  } else {
    _state_1 = 0;
    if (_state_7) {
      if (_s.b) {
        goto N16;
      } else {
        _state_7 = 1;
        _term_21 &= -(1 << 1);
      }
    } else {
    N16:
      _state_7 = 0;
      /* Vacuous terminate */;
    }
    if (_state_3) {
      if (_s.a) {
        goto N19;
      } else {
        _state_3 = 1;
        _term_21 &= -(1 << 1);
      }
    } else {
    N19:
      _state_3 = 0;
      /* Vacuous terminate */;
    }
    if (~_term_21) {
    } else {
      _s.o = 1;
      _state_1 = 0;
      /* Vacuous terminate */;
      /* Vacuous terminate */;
      _state_7 = 1;
      _state_3 = 1;
    }
  }
  if (_s.o) { DRIVE_O_o(); _s.o = 0; }
  _s.a = 0;
  _s.b = 0;
  return 1;
}

int DRIVE_reset(void)
{
  _s.a = 0;
  _s.b = 0;
  return 0;
}
